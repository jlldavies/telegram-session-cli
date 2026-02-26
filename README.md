# Telegram Session String Generator

> A standalone Python script that walks you through generating a Telethon `StringSession` — the credential string required by automation tools that connect to Telegram as a user account.

[Installation](#installation) • [Features](#features) • [How It Works](#how-it-works) • [References](#references)

---

## The Problem

Tools that automate Telegram (n8n, bots, scrapers, workflow engines) need a **session string** to authenticate as a real user account. Getting one involves:

- Creating a Telegram API app at `my.telegram.org`
- Connecting to Telegram's MTProto API with the right credentials
- Handling 2FA, verification codes, rate limits, and multiple delivery methods

Most guides assume technical knowledge and give no help when things go wrong.

## The Solution

A single script your colleague can run. It asks the right questions, tells you exactly what Telegram sent back at every step, and gives a plain-English fix for every error — including when the verification code doesn't arrive.

```
python3 telegram_session.py
```

That's it. At the end you get your **API ID**, **API Hash**, and **Session String** on screen, ready to copy.

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

The script walks through four steps:

**Step 0 — Dependency check**
Verifies `telethon` is installed. If not, prints the exact `pip install` command and exits cleanly.

**Step 1 — API Credentials**
Asks whether you already have your API ID and Hash.
- If yes: enter them directly
- If no: on-screen instructions send you to `https://my.telegram.org/apps` to get them (takes ~2 minutes)

**Step 2 — Phone number**
Validates format and country code before connecting.

**Step 3 — Session string generation**
Connects to Telegram's API, requests a sign-in code, and shows you a full debug dump of every field Telegram returned — including exactly how and where the code was delivered:

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
     This goes to every device where you're logged into Telegram.
     It does NOT come as an SMS.
```

If the code doesn't arrive, you can resend via an alternative method or **force SMS delivery** (bypasses app notification entirely using a raw `SendCodeRequest` with `CodeSettings(allow_app=False)`).

---

## Features

**Single dependency**
Only `telethon` — no `requests`, no `beautifulsoup4`, no setup overhead.

**Full Telegram response dump**
Every field from the `SentCode` response is printed — `phone_code_hash`, `timeout`, delivery type with all attributes, and `next_type`. No guessing what Telegram actually sent back.

**All delivery types decoded**
Handles and explains every known `SentCodeType`:
- `SentCodeTypeApp` — in-app notification
- `SentCodeTypeSms` — SMS text
- `SentCodeTypeCall` — voice call
- `SentCodeTypeFlashCall` — flash call
- `SentCodeTypeMissedCall` — missed call (code = last digits of calling number)
- `SentCodeTypeEmailCode` — email
- `SentCodeTypeFragmentSms` — anonymous Fragment numbers
- `SentCodeTypeFirebaseSms` — Firebase delivery
- Unknown future types — raw attribute dump

**Force SMS option**
When Telegram defaults to app delivery and the code doesn't arrive, option `[3]` fires a raw `SendCodeRequest` with `CodeSettings(allow_app=False)` to force SMS instead.

**Every error caught and explained**
Specific handling for all known Telethon errors on every code path:

| Error | Plain English message + fix |
|-------|-----------------------------|
| `PhoneNumberInvalidError` | Number format wrong |
| `PhoneNumberBannedError` | Account banned |
| `PhoneNumberUnoccupiedError` | No Telegram account for this number |
| `PhoneNumberFloodError` | Too many requests today |
| `ApiIdInvalidError` | Wrong API credentials |
| `ApiIdPublishedFloodError` | API ID leaked/flagged |
| `FloodWaitError` | Rate limited — shows exact wait time |
| `AuthRestartError` | Broken session state |
| `PhoneMigrateError` / `NetworkMigrateError` | DC redirect |
| `PhoneCodeInvalidError` | Wrong code entered |
| `PhoneCodeExpiredError` | Code timed out |
| `SessionPasswordNeededError` | 2FA — prompts for cloud password |
| `PasswordHashInvalidError` | Wrong 2FA password |

**2FA support**
Detects Two-Factor Authentication automatically and prompts for the cloud password with recovery instructions if forgotten.

**Screen stays open**
Every exit path — success or error — ends with `Press Enter to exit` so the terminal window doesn't vanish before the output is read.

---

## Security

The session string, API ID, and API Hash give **full access to the Telegram account**. Treat them like a password:

- Do not commit them to version control
- Do not share them in chat, email, or documents
- Store them in a secrets manager or environment variable in any tool that uses them

---

## References

- [Telethon Documentation](https://docs.telethon.dev/en/stable/)
- [Telethon StringSession](https://docs.telethon.dev/en/stable/modules/sessions.html#telethon.sessions.string.StringSession)
- [Telegram API — auth.sendCode](https://core.telegram.org/method/auth.sendCode)
- [Telegram API — CodeSettings](https://core.telegram.org/constructor/codeSettings)
- [Telegram API — auth.SentCode](https://core.telegram.org/constructor/auth.sentCode)
- [my.telegram.org — Create an App](https://my.telegram.org/apps)

---

*Built to solve a real problem: getting a session string without needing to understand MTProto.*
