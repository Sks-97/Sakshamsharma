/**
 * Email Queue — sends approved rows from a Google Sheet as the script owner.
 *
 * Deploy this as a STANDALONE Apps Script project (script.google.com), NOT as a
 * script bound to the sheet. Anyone with edit access to a sheet can open and
 * rewrite its bound script, and that rewritten code then runs under the account
 * of whoever owns the trigger. Standalone keeps the code out of their reach.
 */

// ---------------------------------------------------------------- config

var SHEET_ID   = '19zQjjArR1uMeCAbMur3-2xt5zak6lDK7bSdBTfXPgew';
var TAB_NAME   = '';   // '' = first tab
var MAX_PER_RUN = 25;  // leaves headroom under the daily Gmail quota
var SENDER_NAME = 'Radhika Malhan';
var REPLY_TO    = '';  // '' = your account address

var FIRST_DATA_ROW = 2;
var COL = { ID: 1, TO: 2, CC: 3, SUBJECT: 4, BODY: 5, APPROVED: 6, STATUS: 7, SENT_AT: 8, NOTES: 9 };

// ---------------------------------------------------------------- main

/** Trigger entry point. Sends every approved, not-yet-sent row. */
function sendApprovedEmails() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) {
    Logger.log('Another run holds the lock; exiting.');
    return;
  }

  try {
    var sheet = getSheet_();
    var last = sheet.getLastRow();
    if (last < FIRST_DATA_ROW) { Logger.log('No data rows.'); return; }

    var rows = sheet.getRange(FIRST_DATA_ROW, 1, last - FIRST_DATA_ROW + 1, COL.NOTES).getValues();
    var quota = MailApp.getRemainingDailyQuota();
    var sent = 0, failed = 0, skipped = 0;

    for (var i = 0; i < rows.length; i++) {
      if (sent >= MAX_PER_RUN) { Logger.log('Hit MAX_PER_RUN; remaining rows wait for the next run.'); break; }
      if (sent >= quota)       { Logger.log('Out of daily Gmail quota; remaining rows wait for tomorrow.'); break; }

      var rowNum = FIRST_DATA_ROW + i;
      var row    = rows[i];

      if (!isApproved_(row[COL.APPROVED - 1])) { skipped++; continue; }
      if (String(row[COL.STATUS - 1]).trim() !== '') { skipped++; continue; }  // already SENT / SENDING / ERROR

      var mail = buildMessage_(row);
      if (mail.error) {
        writeResult_(sheet, rowNum, 'ERROR', mail.error);
        failed++;
        continue;
      }

      // Claim the row BEFORE sending. If the script dies mid-send the row reads
      // SENDING, not blank, so the next run won't send it a second time.
      writeResult_(sheet, rowNum, 'SENDING', '');

      try {
        GmailApp.sendEmail(mail.to, mail.subject, mail.body, mail.options);
        writeResult_(sheet, rowNum, 'SENT', '');
        sent++;
      } catch (err) {
        writeResult_(sheet, rowNum, 'ERROR', String(err));
        failed++;
      }
    }

    Logger.log('sent=%s failed=%s skipped=%s', sent, failed, skipped);
  } finally {
    lock.releaseLock();
  }
}

/** Dry run: logs exactly what sendApprovedEmails would do, sending nothing. */
function previewApprovedEmails() {
  var sheet = getSheet_();
  var last = sheet.getLastRow();
  if (last < FIRST_DATA_ROW) { Logger.log('No data rows.'); return; }

  var rows = sheet.getRange(FIRST_DATA_ROW, 1, last - FIRST_DATA_ROW + 1, COL.NOTES).getValues();
  var pending = 0;

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    if (!isApproved_(row[COL.APPROVED - 1])) continue;
    if (String(row[COL.STATUS - 1]).trim() !== '') continue;

    var mail = buildMessage_(row);
    pending++;
    if (mail.error) {
      Logger.log('row %s  WOULD FAIL — %s', FIRST_DATA_ROW + i, mail.error);
    } else {
      Logger.log('row %s  -> %s%s  |  %s', FIRST_DATA_ROW + i, mail.to,
                 mail.options.cc ? ' (cc ' + mail.options.cc + ')' : '', mail.subject);
    }
  }
  Logger.log('%s row(s) pending. Daily quota left: %s', pending, MailApp.getRemainingDailyQuota());
}

// ---------------------------------------------------------------- helpers

function getSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = TAB_NAME ? ss.getSheetByName(TAB_NAME) : ss.getSheets()[0];
  if (!sheet) throw new Error('Tab not found: ' + TAB_NAME);
  return sheet;
}

/** Validates one row and assembles the Gmail payload. Returns {error} on bad input. */
function buildMessage_(row) {
  var to      = String(row[COL.TO - 1]).trim();
  var subject = String(row[COL.SUBJECT - 1]).trim();
  var body    = String(row[COL.BODY - 1]);

  if (!to)      return { error: 'No recipient in the To column.' };
  if (!subject) return { error: 'No subject.' };
  if (!body.trim()) return { error: 'No body.' };

  var recipients = splitAddresses_(to);
  for (var i = 0; i < recipients.length; i++) {
    if (!isEmail_(recipients[i])) return { error: 'Not a valid address: ' + recipients[i] };
  }

  var options = { name: SENDER_NAME };
  if (REPLY_TO) options.replyTo = REPLY_TO;

  var ccRaw = String(row[COL.CC - 1]).trim();
  if (ccRaw) {
    var cc = splitAddresses_(ccRaw);
    for (var j = 0; j < cc.length; j++) {
      if (!isEmail_(cc[j])) return { error: 'Not a valid CC address: ' + cc[j] };
    }
    options.cc = cc.join(',');
  }

  // Sent as plain text, so the line and paragraph breaks she typed in the cell
  // survive exactly as written.
  return { to: recipients.join(','), subject: subject, body: body, options: options };
}

function splitAddresses_(value) {
  return String(value).split(/[,;]/).map(function (s) { return s.trim(); })
                      .filter(function (s) { return s !== ''; });
}

function isEmail_(value) {
  return /^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]{2,}$/.test(value);
}

function isApproved_(value) {
  if (value === true) return true;
  var s = String(value).trim().toLowerCase();
  return s === 'yes' || s === 'y' || s === 'true' || s === 'approved' || s === '✓';
}

function writeResult_(sheet, rowNum, status, note) {
  sheet.getRange(rowNum, COL.STATUS).setValue(status);
  sheet.getRange(rowNum, COL.SENT_AT).setValue(status === 'SENT' ? new Date() : '');
  if (note) sheet.getRange(rowNum, COL.NOTES).setValue(note);
  SpreadsheetApp.flush();  // persist immediately; don't batch across sends
}

// ---------------------------------------------------------------- setup

/** Run once to start the timer. Safe to re-run — it clears old triggers first. */
function installTrigger() {
  removeTriggers();
  ScriptApp.newTrigger('sendApprovedEmails').timeBased().everyMinutes(15).create();
  Logger.log('Trigger installed: every 15 minutes.');
}

function removeTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'sendApprovedEmails') ScriptApp.deleteTrigger(t);
  });
}
