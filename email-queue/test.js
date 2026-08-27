const fs = require('fs'), vm = require('vm');
const SRC = fs.readFileSync('/home/user/Sakshamsharma/email-queue/Code.gs', 'utf8');

const HEADER = ['Row ID','To','CC','Subject','Body','Approved','Status','Sent At','Notes'];

function makeSheet(dataRows) {
  const grid = [HEADER.slice(), ...dataRows.map(r => r.slice())];
  return {
    grid,
    getLastRow: () => grid.length,
    getRange(row, col, numRows, numCols) {
      if (numRows === undefined) {
        return { setValue: v => { grid[row-1][col-1] = v; },
                 getValue: () => grid[row-1][col-1] };
      }
      return { getValues: () => grid.slice(row-1, row-1+numRows).map(r => r.slice(col-1, col-1+numCols)) };
    }
  };
}

function run(dataRows, opts = {}) {
  const sheet = makeSheet(dataRows);
  const sends = [];
  const logs  = [];
  const ctx = {
    SpreadsheetApp: { openById: () => ({ getSheets: () => [sheet], getSheetByName: () => sheet }), flush: () => {} },
    GmailApp: {
      sendEmail: (to, subject, body, options) => {
        if (opts.throwOn && opts.throwOn(to)) throw new Error('SMTP boom');
        sends.push({ to, subject, body, options });
      },
      getAliases: () => (opts.aliases === undefined ? ['hi@radmalhan.com'] : opts.aliases),
    },
    Session: { getActiveUser: () => ({
      getEmail: () => (opts.activeUser === undefined ? 'radhika.malhan@gmail.com' : opts.activeUser),
    })},
    MailApp: { getRemainingDailyQuota: () => (opts.quota === undefined ? 100 : opts.quota) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock: () => {} }) },
    Logger: { log: (...a) => logs.push(a.join(' ')) },
    ScriptApp: { getProjectTriggers: () => [], newTrigger: () => ({ timeBased: () => ({ everyMinutes: () => ({ create: () => {} }) }) }) },
    Date,
  };
  vm.createContext(ctx);
  let error = null;
  try { vm.runInContext(SRC + '\nsendApprovedEmails();', ctx); }
  catch (e) { error = e; }
  return { sheet, sends, logs, error };
}

let pass = 0, fail = 0;
const ok = (name, cond, extra) => {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else { fail++; console.log('  FAIL  ' + name + (extra ? '\n          ' + extra : '')); }
};
const S = 6, ST = 7, SA = 8, N = 9; // 1-indexed approved/status/sentat/notes

console.log('\n--- happy path ---');
{
  const { sheet, sends } = run([[1,'jane@example.com','','Hello','Line one\n\nLine two','YES','','','']]);
  ok('sent exactly one', sends.length === 1, 'got ' + sends.length);
  ok('correct recipient', sends[0] && sends[0].to === 'jane@example.com');
  ok('body newlines preserved', sends[0] && sends[0].body === 'Line one\n\nLine two',
     JSON.stringify(sends[0] && sends[0].body));
  ok('status = SENT', sheet.grid[1][ST-1] === 'SENT', String(sheet.grid[1][ST-1]));
  ok('timestamp written', sheet.grid[1][SA-1] instanceof Date);
}

console.log('\n--- not approved is left alone ---');
{
  const { sheet, sends } = run([[1,'jane@example.com','','Hello','Body','','','','']]);
  ok('nothing sent', sends.length === 0);
  ok('status still blank', sheet.grid[1][ST-1] === '');
}

console.log('\n--- already SENT is never resent ---');
{
  const { sends } = run([[1,'jane@example.com','','Hello','Body','YES','SENT','','']]);
  ok('nothing sent', sends.length === 0, 'got ' + sends.length);
}

console.log('\n--- idempotency: two consecutive runs ---');
{
  const rows = [[1,'jane@example.com','','Hello','Body','YES','','','']];
  const first = run(rows);
  // feed the post-run grid straight back in, as the next trigger would see it
  const after = first.sheet.grid.slice(1);
  const second = run(after);
  ok('run 1 sends once', first.sends.length === 1);
  ok('run 2 sends nothing', second.sends.length === 0, 'got ' + second.sends.length);
}

console.log('\n--- validation ---');
{
  const { sheet, sends } = run([
    [1,'not-an-email','','Hello','Body','YES','','',''],
    [2,'ok@example.com','','','Body','YES','','',''],
    [3,'ok@example.com','','Subject','','YES','','',''],
    [4,'','','Subject','Body','YES','','',''],
  ]);
  ok('no bad row sent', sends.length === 0, 'got ' + sends.length);
  ok('bad address -> ERROR', sheet.grid[1][ST-1] === 'ERROR');
  ok('bad address note',    /not a valid address/i.test(String(sheet.grid[1][N-1])), String(sheet.grid[1][N-1]));
  ok('no subject -> ERROR', sheet.grid[2][ST-1] === 'ERROR');
  ok('no body -> ERROR',    sheet.grid[3][ST-1] === 'ERROR');
  ok('no recipient -> ERROR', sheet.grid[4][ST-1] === 'ERROR');
}

console.log('\n--- CC + multiple recipients ---');
{
  const { sends } = run([[1,'a@example.com, b@example.com','c@example.com; d@example.com','S','B','YES','','','']]);
  ok('to joined', sends[0] && sends[0].to === 'a@example.com,b@example.com', sends[0] && sends[0].to);
  ok('cc joined', sends[0] && sends[0].options.cc === 'c@example.com,d@example.com', sends[0] && sends[0].options.cc);
}

console.log('\n--- approved spellings ---');
{
  const { sends } = run([
    [1,'a@example.com','','S','B','yes','','',''],
    [2,'b@example.com','','S','B','Y','','',''],
    [3,'c@example.com','','S','B',true,'','',''],
    [4,'d@example.com','','S','B','TRUE','','',''],
    [5,'e@example.com','','S','B','approved','','',''],
    [6,'f@example.com','','S','B','maybe','','',''],
    [7,'g@example.com','','S','B','no','','',''],
  ]);
  ok('5 accepted, 2 rejected', sends.length === 5, 'got ' + sends.length);
  ok('"maybe"/"no" not sent', !sends.some(s => /^[fg]@/.test(s.to)));
}

console.log('\n--- send failure is recorded, not retried blindly ---');
{
  const { sheet, sends } = run(
    [[1,'boom@example.com','','S','B','YES','','',''],
     [2,'fine@example.com','','S','B','YES','','','']],
    { throwOn: to => to === 'boom@example.com' });
  ok('good row still sent', sends.length === 1 && sends[0].to === 'fine@example.com');
  ok('failed row -> ERROR', sheet.grid[1][ST-1] === 'ERROR', String(sheet.grid[1][ST-1]));
  ok('error message captured', /boom/i.test(String(sheet.grid[1][N-1])), String(sheet.grid[1][N-1]));
  // both rows now carry a status (ERROR / SENT), so a re-run must send nothing
  ok('neither row resent next run', run(sheet.grid.slice(1)).sends.length === 0);
}

console.log('\n--- sender identity ---');
{
  const row = () => [[1,'jane@example.com','','S','B','YES','','','']];

  const verified = run(row());
  ok('verified alias -> from is set',
     verified.sends[0] && verified.sends[0].options.from === 'hi@radmalhan.com',
     JSON.stringify(verified.sends[0] && verified.sends[0].options));
  ok('verified alias -> no error', verified.error === null);

  // The critical case: Gmail would silently fall back to the primary address.
  const unverified = run(row(), { aliases: ['other@example.com'] });
  ok('unverified alias -> throws', unverified.error !== null);
  ok('unverified alias -> sends NOTHING', unverified.sends.length === 0,
     'got ' + unverified.sends.length);
  ok('unverified alias -> row left untouched', unverified.sheet.grid[1][ST-1] === '',
     String(unverified.sheet.grid[1][ST-1]));
  ok('error names the offending address',
     /hi@radmalhan\.com/.test(String(unverified.error)), String(unverified.error));
  ok('error names what it would have sent from',
     /radhika\.malhan@gmail\.com/.test(String(unverified.error)));

  const noAliases = run(row(), { aliases: [] });
  ok('no aliases at all -> throws, sends nothing',
     noAliases.error !== null && noAliases.sends.length === 0);

  // Script running under hi@ itself: no override needed, and none should be set.
  const native = run(row(), { aliases: [], activeUser: 'hi@radmalhan.com' });
  ok('script owned by hi@ -> sends without error', native.error === null && native.sends.length === 1,
     String(native.error));
  ok('script owned by hi@ -> no from override', native.sends[0] && !native.sends[0].options.from);

  const caseInsensitive = run(row(), { aliases: ['HI@RadMalhan.com'] });
  ok('alias match is case-insensitive', caseInsensitive.error === null && caseInsensitive.sends.length === 1);
}

console.log('\n--- quota exhaustion stops the run ---');
{
  const rows = Array.from({length: 5}, (_, i) => [i+1, `u${i}@example.com`,'','S','B','YES','','','']);
  const { sends } = run(rows, { quota: 2 });
  ok('stops at quota', sends.length === 2, 'got ' + sends.length);
}

console.log(`\n${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
