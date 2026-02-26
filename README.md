# Telegram Session String Generator

> A diagnostic-first script for getting a Telethon `StringSession` — built for people who are struggling to connect Telegram to an MCP, automation tool, or workflow engine and need to see exactly what's going wrong.

[The Problem](#the-problem) • [Installation](#installation) • [How It Works](#how-it-works) • [Features](#features) • [References](#references)

---

## The Problem

Most tools that connect Telegram to MCPs, n8n, bots, or other automation platforms need a **session string** to authenticate as a real user account. Getting one should be simple — but in practice it regularly fails, and when it does the tools give you almost nothing to work with:

- Sign-in codes that silently never arrive
- No indication of *how* the code was sent (app notification? SMS? voice call?)
- Generic errors with no fix instructions
- Processes that just hang or exit without explanation

If you've ever stared at a blank terminal wondering why your Telegram MCP isn't connecting, this script is for you.

## The Solution

A standalone Python script with **one dependency** that walks through every step of the connection process out loud — showing you the raw Telegram API response, exactly where your code was sent, what every field means, and a plain-English fix for every error that can occur.

```
python3 telegram_session.py
```

At the end you get your **API ID**, **API Hash**, and **Session String** — ready to paste into whichever tool you're connecting.

---

## Installation

**One dependency:**

```bash
pip install telethon
```

**Then run:**

```bash
python3 telegram_session.py
```

No virtual environment needed. No config files. No `.env`. Just Python 3 and one package.

---

## How It Works

The script walks through four steps, printing everything at each stage:

**Step 0 — Dependency check**
Verifies `telethon` is installed. If not, prints the exact `pip install` command and exits cleanly.

**Step 1 — API Credentials**
Asks whether you already have your API ID and Hash.
- If yes: enter them directly
- If no: step-by-step instructions walk you to `https://my.telegram.org/apps` to get them (2 minutes)

**Step 2 — Phone number**
Validates format and country code before any connection is attempted.

**Step 3 — Session string generation**
Connects to Telegram's API, requests a sign-in code, and immediately shows a full dump of everything Telegram sent back — so you can see exactly what happened and where to look for the code:

```
── Telegram response (full debug dump) ──────────────────
  phone_code_hash :  a1b2c3d4e5f6a7b8c9d0
  timeout         :  300s  (5m 0s)
  type (raw)      :  SentCodeTypeApp
    .length       :  5
  next_type (raw) :  SentCodeTypeSms
    .length       :  5
─────────────────────────────────────────────────────────

  Where your code was sent:

     Telegram APP notification  (code is 5 digits)
     Look for a message from the official 'Telegram' account inside the app
     This goes to every device where you're logged into Telegram —
     phone, tablet, desktop, web.
     It does NOT come as an SMS.
```

If the code still doesn't arrive, there are two further options: resend via the alternative method shown in `next_type`, or **force SMS delivery** via a raw `SendCodeRequest` with `CodeSettings(allow_app=False)` — bypassing app notification entirely.

---

## Features

**Verbose by design**
Every step prints what it's doing, what Telegram responded, and what it means in plain English. Nothing is silent.

**Full Telegram response dump**
Every field from the `SentCode` response is shown — `phone_code_hash`, `timeout`, delivery type and all its attributes, and `next_type`. You can see at a glance whether Telegram received the request and what delivery method it chose.

**All delivery types decoded**
Handles and explains every known `SentCodeType` with human-readable instructions:
- `SentCodeTypeApp` — in-app notification (the most common, and the most commonly missed)
- `SentCodeTypeSms` — SMS text message
- `SentCodeTypeCall` — voice call
- `SentCodeTypeFlashCall` — flash call
- `SentCodeTypeMissedCall` — missed call (code = last digits of the calling number)
- `SentCodeTypeEmailCode` — email code
- `SentCodeTypeFragmentSms` — anonymous Fragment numbers
- `SentCodeTypeFirebaseSms` — Firebase delivery
- Unknown future types — raw attribute dump so nothing is hidden

**Force SMS option**
When Telegram defaults to app delivery and `next_type` is `none` (no automatic fallback), option `[3]` fires a raw `SendCodeRequest` with `CodeSettings(allow_app=False)` to force SMS regardless.

**Every error caught with a fix**
Specific handling — with plain-English explanations and next steps — for every known Telethon error:

| Error | What it means + what to do |
|-------|----------------------------|
| `PhoneNumberInvalidError` | Number format wrong — check country code |
| `PhoneNumberBannedError` | Account banned from Telegram |
| `PhoneNumberUnoccupiedError` | No Telegram account for this number |
| `PhoneNumberFloodError` | Too many code requests today — wait 24h |
| `ApiIdInvalidError` | Wrong API credentials — re-copy from my.telegram.org |
| `ApiIdPublishedFloodError` | API ID has been flagged — create a new app |
| `FloodWaitError` | Rate limited — shows exact seconds to wait |
| `AuthRestartError` | Broken session — re-run script |
| `PhoneMigrateError` / `NetworkMigrateError` | DC redirect — re-run, Telethon handles it |
| `AuthKeyInvalidError` | Corrupt session — re-run for fresh session |
| `PhoneCodeInvalidError` | Wrong code entered |
| `PhoneCodeExpiredError` | Code timed out — re-run and enter it quickly |
| `SessionPasswordNeededError` | 2FA enabled — prompts for cloud password |
| `PasswordHashInvalidError` | Wrong 2FA password |

**2FA support**
Detects Two-Factor Authentication automatically and prompts for the cloud password, with recovery path if forgotten.

**Screen stays open**
Every exit path — success or error — ends with `Press Enter to exit` so nothing disappears before it's been read.

---

## Security

The session string, API ID, and API Hash give **full access to the Telegram account**. Treat them like a password:

- Do not commit them to version control
- Do not share them in a chat, email, or document
- Store them in a secrets manager or environment variable in the tool that uses them

---

## References

- [Telethon Documentation](https://docs.telethon.dev/en/stable/)
- [Telethon StringSession](https://docs.telethon.dev/en/stable/modules/sessions.html#telethon.sessions.string.StringSession)
- [Telegram API — auth.sendCode](https://core.telegram.org/method/auth.sendCode)
- [Telegram API — CodeSettings](https://core.telegram.org/constructor/codeSettings)
- [Telegram API — auth.SentCode](https://core.telegram.org/constructor/auth.sentCode)
- [my.telegram.org — Create an App](https://my.telegram.org/apps)

---

*Built for people who just want to know why Telegram isn't connecting — not another tool that silently fails.*
