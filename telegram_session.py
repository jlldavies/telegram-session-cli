#!/usr/bin/env python3
"""
Telegram Session String Generator
───────────────────────────────────────────────────────────
Only one dependency:   pip install telethon
───────────────────────────────────────────────────────────
"""

import os, sys

# ── ANSI colours ──────────────────────────────────────────
R  = "\033[0m"
G  = "\033[32;1m"
Y  = "\033[33;1m"
C  = "\033[36;1m"
RE = "\033[31;1m"
W  = "\033[37;1m"
B  = "\033[34;1m"
DIM= "\033[2m"

# ── Helpers ───────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def step(n, title):
    print(f"\n{C}━━━ Step {n}: {title}{R}")

def ok(msg):   print(f"  {G}✓{R}  {msg}")
def info(msg): print(f"  {B}ℹ{R}  {DIM}{msg}{R}")
def warn(msg): print(f"  {Y}!{R}  {Y}{msg}{R}")

def fatal(msg, fix=None):
    print(f"\n  {RE}✗  ERROR:{R}  {msg}")
    if fix:
        print(f"\n  {Y}→  WHAT TO DO:{R}\n")
        for line in fix.strip().split("\n"):
            print(f"     {line}")
    print()
    input(f"\n  {DIM}Press Enter to exit…{R}")
    sys.exit(1)

def banner():
    clear()
    print(f"""{G}
  ████████╗ ██████╗      ███████╗███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗
     ██╔══╝██╔════╝      ██╔════╝██╔════╝██╔════╝██╔════╝██║██╔═══██╗████╗  ██║
     ██║   ██║  ███╗     ███████╗█████╗  ███████╗███████╗██║██║   ██║██╔██╗ ██║
     ██║   ██║   ██║     ╚════██║██╔══╝  ╚════██║╚════██║██║██║   ██║██║╚██╗██║
     ██║   ╚██████╔╝     ███████║███████╗███████║███████║██║╚██████╔╝██║ ╚████║
     ╚═╝    ╚═════╝      ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
{R}{W}                    Session String Generator{R}
{DIM}        Generates a Telethon session string for use with automation tools{R}
""")


# ── Step 0: check the one dependency ─────────────────────
def check_telethon():
    step(0, "Checking dependencies")
    try:
        import telethon
        ok(f"telethon {telethon.__version__} found")
    except ImportError:
        fatal(
            "telethon is not installed.",
            "Open a terminal / command prompt and run:\n\n          pip install telethon\n\n     Then run this script again."
        )


# ── Step 1: get API credentials ───────────────────────────
def get_api_credentials():
    step(1, "API Credentials")
    print(f"""
  {W}You need your Telegram API ID and Hash.{R}
  {DIM}These are free and tied to your Telegram account — not a bot token.{R}

  How to get them ({Y}takes about 2 minutes{R}):

    1. Open  {Y}https://my.telegram.org/apps{R}  in your browser
    2. Log in with your phone number (Telegram sends you a code)
    3. If you see "Create application", click it — fill in anything, it doesn't matter
    4. You'll see {Y}App api_id{R}  (a short number) and {Y}App api_hash{R}  (a long code)
    5. Copy both, come back here, and paste them below
""")
    input(f"  {DIM}Press Enter when you have them ready…{R}\n")

    api_id_str = input(f"  {Y}App api_id   (numbers only): {R}").strip()
    api_hash   = input(f"  {Y}App api_hash (32 characters): {R}").strip()

    if not api_id_str.isdigit():
        fatal(
            f"API ID should be all numbers — you entered: '{api_id_str}'",
            "Go back to https://my.telegram.org/apps\nThe api_id is the short number, e.g.  1234567"
        )
    if len(api_hash) != 32:
        fatal(
            f"API Hash should be exactly 32 characters — yours is {len(api_hash)}.",
            "Go back to https://my.telegram.org/apps\nCopy the full api_hash — it looks like:  a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
        )

    ok(f"API ID:    {api_id_str}")
    ok(f"API Hash:  {api_hash}")
    return int(api_id_str), api_hash


# ── Step 2: phone number ──────────────────────────────────
def get_phone():
    step(2, "Your phone number")
    info("Must include your country code")
    info("UK example:  +447712345678    US example:  +12025550123")

    phone = input(f"\n  {Y}Phone number: {R}").strip()

    if not phone.startswith("+"):
        fatal(
            f"Phone number must start with + and your country code — you entered: '{phone}'",
            "Examples:\n  +447712345678  (UK — starts with +44)\n  +12025550123   (US — starts with +1)\n  +353871234567  (Ireland — starts with +353)"
        )
    return phone


# ── Step 3: generate the session string ──────────────────
def decode_code_type(t, phone):
    """Return a human-readable description of a SentCodeType* object."""
    # Import every known type — older telethon versions may not have them all
    import telethon.tl.types as tlt
    name  = type(t).__name__

    if   name == "SentCodeTypeApp":
        length = getattr(t, "length", "?")
        return (
            f"{G}Telegram APP notification{R}  (code is {length} digits)\n"
            f"     {W}Look for a message from the official 'Telegram' account inside the app{R}\n"
            f"     {DIM}This goes to every device where you're logged into Telegram — "
            f"phone, tablet, desktop, web.{R}\n"
            f"     {DIM}It does NOT come as an SMS.{R}"
        )
    elif name == "SentCodeTypeSms":
        length = getattr(t, "length", "?")
        return (
            f"{G}SMS text message{R}  to {phone}  (code is {length} digits)\n"
            f"     {DIM}Check your phone's messages app.{R}"
        )
    elif name == "SentCodeTypeCall":
        length = getattr(t, "length", "?")
        return (
            f"{G}Voice call{R}  to {phone}  (code is {length} digits)\n"
            f"     {DIM}Answer the call — a robot will read the digits aloud.{R}"
        )
    elif name == "SentCodeTypeFlashCall":
        pattern = getattr(t, "pattern", "?")
        return (
            f"{G}Flash call{R}  to {phone}  (pattern: {pattern})\n"
            f"     {DIM}Telegram calls your number briefly — you don't need to answer.{R}\n"
            f"     {DIM}The code is derived from the calling number pattern.{R}"
        )
    elif name == "SentCodeTypeMissedCall":
        prefix = getattr(t, "prefix_digit_count", "?")
        return (
            f"{G}Missed call{R}  to {phone}\n"
            f"     {DIM}Telegram will ring and hang up. The last {prefix} digits of the "
            f"calling number are your code.{R}"
        )
    elif name == "SentCodeTypeEmailCode":
        length  = getattr(t, "length", "?")
        email   = getattr(t, "email_pattern", "your email")
        return (
            f"{G}Email code{R}  to {email}  (code is {length} digits)\n"
            f"     {DIM}Check your inbox (and spam folder).{R}"
        )
    elif name == "SentCodeTypeSetUpEmailRequired":
        return (
            f"{Y}Email setup required{R}\n"
            f"     {DIM}Telegram wants you to add an email address before it will send codes.{R}\n"
            f"     Open Telegram → Settings → Privacy and Security → Email and add one."
        )
    elif name == "SentCodeTypeFragmentSms":
        length = getattr(t, "length", "?")
        url    = getattr(t, "url", "https://fragment.com")
        return (
            f"{G}Fragment SMS{R}  (code is {length} digits)\n"
            f"     {DIM}This number is anonymous — the code appears at: {url}{R}"
        )
    elif name == "SentCodeTypeFirebaseSms":
        length = getattr(t, "length", "?")
        return (
            f"{G}Firebase SMS{R}  to {phone}  (code is {length} digits)\n"
            f"     {DIM}Check your phone's messages app.{R}"
        )
    else:
        # Unknown future type — show everything we know
        attrs = {k: v for k, v in vars(t).items() if not k.startswith("_")}
        return f"{Y}Unknown delivery method:{R}  {name}\n     Raw data: {attrs}"


def dump_sent(sent, phone):
    """Print every field Telegram returned in the SentCode response."""
    print(f"\n  {C}── Telegram response (full debug dump) ──────────────────{R}")

    # phone_code_hash
    pch = getattr(sent, "phone_code_hash", None)
    print(f"  {DIM}phone_code_hash :{R}  {pch}")

    # timeout
    timeout = getattr(sent, "timeout", None)
    if timeout is not None:
        print(f"  {DIM}timeout         :{R}  {timeout}s  ({timeout // 60}m {timeout % 60}s)")
    else:
        print(f"  {DIM}timeout         :{R}  not provided")

    # type
    print(f"  {DIM}type (raw)      :{R}  {type(sent.type).__name__}")
    type_attrs = {k: v for k, v in vars(sent.type).items() if not k.startswith("_")}
    for k, v in type_attrs.items():
        print(f"  {DIM}  .{k:<14}:{R}  {v}")

    # next_type
    if sent.next_type is not None:
        print(f"  {DIM}next_type (raw) :{R}  {type(sent.next_type).__name__}")
        next_attrs = {k: v for k, v in vars(sent.next_type).items() if not k.startswith("_")}
        for k, v in next_attrs.items():
            print(f"  {DIM}  .{k:<14}:{R}  {v}")
    else:
        print(f"  {DIM}next_type       :{R}  none (no fallback delivery available)")

    print(f"  {C}─────────────────────────────────────────────────────────{R}\n")


def generate_session(phone, api_id, api_hash):
    step(3, "Generating your session string")

    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    from telethon.errors import (
        PhoneNumberInvalidError,
        PhoneNumberBannedError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        PhoneCodeEmptyError,
        PhoneCodeHashEmptyError,
        SessionPasswordNeededError,
        PasswordHashInvalidError,
        FloodWaitError,
        FloodPremiumWaitError,
        ApiIdInvalidError,
        ApiIdPublishedFloodError,
        PhoneNumberUnoccupiedError,
        PhoneNumberFloodError,
        AuthRestartError,
        NetworkMigrateError,
        PhoneMigrateError,
        UserMigrateError,
        AuthKeyUnregisteredError,
        AuthKeyInvalidError,
        SessionExpiredError,
        SessionRevokedError,
    )

    # ── Connect ───────────────────────────────────────────
    info("Connecting to Telegram …")
    client = TelegramClient(StringSession(), api_id, api_hash)
    try:
        client.connect()
    except Exception as e:
        fatal(
            f"Could not connect to Telegram.\n     Detail: {type(e).__name__}: {e}",
            "Things to try:\n"
            "  • Check you have an internet connection\n"
            "  • If you use a VPN, try turning it off\n"
            "  • Wait a minute and try again"
        )
    ok("Connected to Telegram")

    # ── Request sign-in code ──────────────────────────────
    info(f"Requesting sign-in code for {phone} …")
    try:
        sent = client.send_code_request(phone)

    except PhoneNumberInvalidError:
        client.disconnect()
        fatal(
            f"Telegram says the phone number is invalid: {phone}",
            "Re-run and enter a valid number with the + and country code.\n"
            "Example: +447712345678"
        )
    except PhoneNumberBannedError:
        client.disconnect()
        fatal(
            "This phone number has been banned by Telegram.",
            "You'll need to use a different phone number."
        )
    except PhoneNumberUnoccupiedError:
        client.disconnect()
        fatal(
            "There is no Telegram account registered to this phone number.",
            "Install the Telegram app, create an account with this number, then re-run."
        )
    except PhoneNumberFloodError:
        client.disconnect()
        fatal(
            "This phone number has been used too many times for code requests today.",
            "Wait 24 hours before trying again with this number."
        )
    except ApiIdInvalidError:
        client.disconnect()
        fatal(
            "Your API ID or Hash was rejected by Telegram as invalid.",
            "Go back to https://my.telegram.org/apps, copy them again carefully, and re-run."
        )
    except ApiIdPublishedFloodError:
        client.disconnect()
        fatal(
            "This API ID has been flagged by Telegram (too many users or publicly leaked).",
            "Create a new app at https://my.telegram.org/apps and use the new API ID and Hash."
        )
    except AuthRestartError:
        client.disconnect()
        fatal(
            "Telegram asked for an auth restart — the session state is broken.",
            "Re-run the script from scratch."
        )
    except (NetworkMigrateError, PhoneMigrateError, UserMigrateError) as e:
        client.disconnect()
        fatal(
            f"Telegram redirected the request to a different data centre ({type(e).__name__}).\n"
            f"     Detail: {e}",
            "Re-run the script — Telethon should handle this automatically on retry."
        )
    except (AuthKeyUnregisteredError, AuthKeyInvalidError):
        client.disconnect()
        fatal(
            "The auth key is invalid or unregistered — the session is corrupt.",
            "Re-run the script — a fresh session will be created."
        )
    except (SessionExpiredError, SessionRevokedError) as e:
        client.disconnect()
        fatal(
            f"The session was {type(e).__name__.replace('Error','').lower()}.",
            "Re-run the script — a fresh session will be created."
        )
    except FloodWaitError as e:
        client.disconnect()
        mins = e.seconds // 60 + 1
        fatal(
            f"Too many code requests — Telegram is blocking you for {e.seconds}s ({mins} min).",
            f"Wait {mins} minutes, then re-run the script."
        )
    except FloodPremiumWaitError as e:
        client.disconnect()
        fatal(
            f"Telegram Premium flood wait: {e.seconds}s.",
            f"Wait {e.seconds // 60 + 1} minutes, then re-run."
        )
    except Exception as e:
        client.disconnect()
        fatal(
            f"Unexpected error requesting the code.\n     Detail: {type(e).__name__}: {e}",
            "Check your API ID and Hash are correct, then re-run."
        )

    # ── Show full Telegram response ───────────────────────
    dump_sent(sent, phone)

    # ── Tell user exactly where to look ──────────────────
    print(f"  {W}Where your code was sent:{R}\n")
    print(f"     {decode_code_type(sent.type, phone)}\n")

    timeout = getattr(sent, "timeout", None)
    if timeout:
        warn(f"Code expires in {timeout} seconds ({timeout // 60}m {timeout % 60}s) — enter it quickly!")
    else:
        warn("Enter the code quickly — codes expire after a few minutes.")

    # ── Fallback delivery info ────────────────────────────
    if sent.next_type is not None:
        next_name = type(sent.next_type).__name__.replace("SentCodeType", "")
        print(f"\n  {DIM}If it doesn't arrive, you can request a resend via: {next_name}{R}")
    else:
        print(f"\n  {DIM}No alternative delivery method available for this number.{R}")

    # ── Resend option ─────────────────────────────────────
    print(f"""
    {G}[1]{R}  I have the code — let me enter it now
    {G}[2]{R}  It didn't arrive — resend via a different method
    {G}[3]{R}  {Y}Force SMS{R} — bypass app delivery, send code as a text message instead
""")
    resend_choice = input(f"  {Y}Enter 1, 2 or 3 (default 1): {R}").strip()

    if resend_choice == "2":
        if sent.next_type is not None:
            info("Requesting resend …")
            try:
                sent = client.resend_code_request(phone, sent.phone_code_hash)
                print()
                ok(f"Code resent.  New method: {type(sent.type).__name__.replace('SentCodeType','')}")
                print(f"\n     {decode_code_type(sent.type, phone)}\n")
                dump_sent(sent, phone)
            except FloodWaitError as e:
                fatal(
                    f"Telegram is rate-limiting resend — wait {e.seconds}s.",
                    f"Re-run the script in {e.seconds // 60 + 1} minutes."
                )
            except Exception as e:
                fatal(
                    f"Resend failed.\n     Detail: {type(e).__name__}: {e}",
                    "Re-run the script and try again."
                )
        else:
            print()
            warn("No standard resend available — try option 3 to force SMS instead.")

    if resend_choice == "3":
        # ── Force SMS via raw SendCodeRequest with allow_app=False ───────────
        from telethon.tl.functions.auth import SendCodeRequest
        from telethon.tl.types import CodeSettings

        info("Requesting code via forced SMS (bypassing app notification) …")
        try:
            sent = client(SendCodeRequest(
                phone_number=phone,
                api_id=api_id,
                api_hash=api_hash,
                settings=CodeSettings(
                    allow_flashcall=False,
                    current_number=False,
                    allow_app=False,
                    allow_missed_call=False,
                )
            ))
            print()
            ok(f"Request sent.  Delivery method: {type(sent.type).__name__.replace('SentCodeType','')}")
            print(f"\n     {decode_code_type(sent.type, phone)}\n")
            dump_sent(sent, phone)
        except FloodWaitError as e:
            fatal(
                f"Rate limited — wait {e.seconds}s.",
                f"Re-run the script in {e.seconds // 60 + 1} minutes."
            )
        except Exception as e:
            fatal(
                f"Force SMS request failed.\n     Detail: {type(e).__name__}: {e}",
                "Telegram may not support SMS for this number.\n"
                "Try logging into https://my.telegram.org in a browser to get a code there instead."
            )

    # ── Enter code ────────────────────────────────────────
    code = input(f"\n  {Y}Enter the code: {R}").strip()

    # ── Sign in ───────────────────────────────────────────
    try:
        client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)

    except PhoneCodeInvalidError:
        client.disconnect()
        fatal(
            "That code is wrong.",
            "Re-run the script and type the code exactly — no spaces, no dots."
        )
    except PhoneCodeExpiredError:
        client.disconnect()
        fatal(
            "That code has expired.",
            "Re-run the script and enter the code as soon as it arrives."
        )
    except PhoneCodeEmptyError:
        client.disconnect()
        fatal(
            "You submitted an empty code.",
            "Re-run and type the digits from your Telegram app."
        )
    except PhoneCodeHashEmptyError:
        client.disconnect()
        fatal(
            "Internal error — phone code hash is missing.",
            "Re-run the script from scratch."
        )
    except SessionPasswordNeededError:
        # ── 2FA ──────────────────────────────────────────
        print()
        ok("This account has Two-Factor Authentication (2FA) enabled.")
        info("Enter the cloud password you set in Telegram → Settings → Privacy → Two-Step Verification.")
        pw = input(f"\n  {Y}2FA password: {R}")
        try:
            client.sign_in(password=pw)
        except PasswordHashInvalidError:
            client.disconnect()
            fatal(
                "Wrong 2FA password.",
                "Re-run and enter the correct password.\n"
                "If you've forgotten it: Telegram → Settings → Privacy and Security → Two-Step Verification → Forgot password"
            )
        except FloodWaitError as e:
            client.disconnect()
            fatal(
                f"Too many 2FA attempts — wait {e.seconds}s.",
                f"Re-run the script in {e.seconds // 60 + 1} minutes."
            )
        except Exception as e:
            client.disconnect()
            fatal(
                f"2FA sign-in failed.\n     Detail: {type(e).__name__}: {e}",
                "Check your password and try again."
            )
        ok("2FA verified")

    except FloodWaitError as e:
        client.disconnect()
        fatal(
            f"Rate limited — Telegram says wait {e.seconds}s.",
            f"Re-run the script in {e.seconds // 60 + 1} minutes."
        )
    except AuthRestartError:
        client.disconnect()
        fatal(
            "Telegram requested an auth restart during sign-in.",
            "Re-run the script from scratch."
        )
    except (AuthKeyUnregisteredError, AuthKeyInvalidError) as e:
        client.disconnect()
        fatal(
            f"Auth key error during sign-in: {type(e).__name__}",
            "Re-run the script — a new session will be created."
        )
    except Exception as e:
        client.disconnect()
        fatal(
            f"Sign-in failed.\n     Detail: {type(e).__name__}: {e}",
            "Re-run the script. If it keeps failing, double-check your API ID and Hash."
        )

    ok("Signed in successfully!")
    session_string = client.session.save()
    client.disconnect()
    return session_string


# ── Done ─────────────────────────────────────────────────
def print_result(api_id, api_hash, session_string):
    clear()
    print(f"""
{G}╔══════════════════════════════════════════════════════════════════════════╗
║                        ALL DONE — copy these out                        ║
╚══════════════════════════════════════════════════════════════════════════╝{R}

  {Y}API ID{R}
  {W}{api_id}{R}

  {Y}API Hash{R}
  {W}{api_hash}{R}

  {Y}Session String  ← copy this entire line, it may be very long{R}
  {G}{session_string}{R}

{RE}  ▲  Keep these private — they give full access to your Telegram account.
  ▲  Do not share them in a chat, email, or document others can see.{R}

{G}══════════════════════════════════════════════════════════════════════════{R}
""")
    input(f"  {DIM}Press Enter to exit…{R}\n")


# ── Main ─────────────────────────────────────────────────
def main():
    banner()
    check_telethon()
    api_id, api_hash = get_api_credentials()
    phone = get_phone()
    session_string = generate_session(phone, api_id, api_hash)
    print_result(api_id, api_hash, session_string)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Y}Cancelled.{R}\n")
        sys.exit(0)
