# Email Queue

Lets an assistant queue up emails in a Google Sheet that go out from the owner's
Gmail address — without giving them access to the mailbox.

- **Sheet:** [Email Queue — Intern](https://docs.google.com/spreadsheets/d/19zQjjArR1uMeCAbMur3-2xt5zak6lDK7bSdBTfXPgew/edit)
- **Script:** `Code.gs` — a standalone Apps Script project
- **Tests:** `node test.js` (runs the script against a fake sheet; no email sent)

## How it works

She fills in `To`, `CC`, `Subject`, `Body`. You put `YES` in `Approved`. Every 15
minutes the script picks up approved rows with an empty `Status`, sends them, and
writes `SENT` plus a timestamp back to the row. Anything malformed gets `ERROR`
and a reason in `Notes` instead of being sent.

The trigger runs under **your** Google account, so mail leaves under your identity
— configured to send as `hi@radmalhan.com`. She never touches Gmail.

## Setup

**1. Prepare the sheet.** Delete the two example rows.

**2. Protect the gate columns.** Select columns `F:I` (Approved, Status, Sent At,
Notes) → right-click → *Protect range* → *Set permissions* → *Only you*. This is
the step that makes the approval gate real; without it she can approve her own rows.

**3. Create the script.** Go to [script.google.com](https://script.google.com) →
*New project* → paste in `Code.gs` → save.

> Create it there, **not** from inside the sheet via Extensions → Apps Script.
> Anyone with edit access to a sheet can rewrite its bound script, and that
> rewritten code then runs under whichever account owns the trigger — yours. A
> standalone project keeps the code out of her reach.

**4. Authorize and confirm the sending address.** Run `checkAliases` once. Google will prompt for
permissions; the "unverified app" warning is expected for your own script
(*Advanced* → *Go to project*). The log tells you which account the script runs as
and which addresses it may legitimately send from. If `hi@radmalhan.com` isn't
listed, fix that first — see below. Then run `previewApprovedEmails`, which sends
nothing and just logs what would go out.

**5. Start the timer.** Run `installTrigger` once.

**6. Share the sheet** with her as an **Editor**.

## Day to day

- **Approve:** put `YES` in `Approved`. Also accepted: `Y`, `TRUE`, `approved`, a ticked checkbox.
- **Hold something back:** leave `Approved` empty. Nothing sends.
- **Retry a failed row:** fix the problem, then clear the `Status` cell. A row keeps
  its `ERROR` until you clear it, so a bad address can't spin in a retry loop.
- **Stop everything:** run `removeTriggers`.

## Settings

At the top of `Code.gs`:

| | |
|---|---|
| `SHEET_ID` | Which sheet to read. Already set. |
| `MAX_PER_RUN` | Cap per run (25). |
| `SENDER_NAME` | Display name on outgoing mail. |
| `SEND_AS` | Address mail is sent from. Empty = the script owner's own address. |
| `REPLY_TO` | Set to route replies elsewhere. Empty = the `SEND_AS` address. |
| `TAB_NAME` | Empty = first tab. |

## Sending from hi@radmalhan.com

`SEND_AS` is set to `hi@radmalhan.com`. Gmail honours a `from` address **only** if
it's a verified send-as alias on the account running the script. Hand it anything
else and Gmail doesn't error — it quietly sends from the account's primary address
instead. So `resolveSendAs_` checks the alias list up front and refuses to run at
all if it doesn't match, rather than letting a whole queue go out under the wrong
name.

Run `checkAliases` to see where you stand. If `hi@radmalhan.com` isn't in the
verified list, pick whichever of these fits how that address is set up:

**If `hi@radmalhan.com` is its own Google account** (a Workspace login), that's the
cleanest fix: build the Apps Script project while signed in as `hi@`, and share the
sheet with it as an **Editor**. It then sends from `hi@` natively, no alias needed —
the script detects this and skips the override.

**If it's a mailbox or forwarder at your domain host**, add it as an alias on the
Gmail account: *Gmail → Settings → Accounts and Import → "Send mail as" → Add
another email address*. Untick "Treat as an alias" if you want replies to land in
the `hi@` mailbox rather than your gmail inbox. Google mails a confirmation code to
`hi@radmalhan.com` — enter it, and the address becomes usable.

One cosmetic caveat: if the alias sends through Gmail's servers rather than your
domain's own SMTP, recipients see `hi@radmalhan.com via gmail.com` in some clients.
Entering your host's SMTP details during alias setup avoids that, and is better for
deliverability on a domain you own.

## Known limits

- **Gmail's daily cap** is 100 recipients/day on a consumer account, 1,500 on
  Workspace. The script stops when the quota runs out and resumes the next day.
- **Body is sent as plain text**, so the line breaks she types are preserved
  exactly. No bold, links, or attachments — those need `htmlBody` and Drive
  attachment handling.
- **There's a window between approval and send.** Since she can edit `To` and
  `Body`, she could in principle change a row after you approve it but before the
  trigger fires. Approving as the last step before a run, or shortening the trigger
  interval, keeps that window small. Protecting `B:E` too closes it entirely, at
  the cost of her not being able to fix typos on queued rows.
