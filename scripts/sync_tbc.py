#!/usr/bin/env python3
"""
Telebotcreator (TBC) Workspace Synchronization Utility.
Synchronizes local command files with Telebotcreator API, pulls online commands,
lists online bot commands, and validates command metadata.
"""

import os
import sys
import re
import json
import base64
import argparse
from pathlib import Path

# Safe import for requests
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' module is missing. Please install it with: pip install requests")
    sys.exit(1)


def load_config(args):
    """
    Load configuration with precedence:
    1. Command line arguments
    2. Environment variables
    3. Custom config file (if specified via --config)
    4. Local workspace config file (./tbc_config.json)
    5. Global config file (~/.gemini/config/tbc_config.json or ~/.tbc_config.json)
    """
    config = {
        "bot_id": None,
        "login_token": None,
        "commands_dir": "commands",
        "api_base_url": "https://api.telebotcreator.com/v2"
    }

    # Potential config file locations
    config_paths = []
    if args.config:
        config_paths.append(Path(args.config))
    else:
        # Local workspace config
        config_paths.append(Path.cwd() / "tbc_config.json")
        # Global config in ~/.gemini/config/
        config_paths.append(Path.home() / ".gemini" / "config" / "tbc_config.json")
        # Global config in home directory
        config_paths.append(Path.home() / ".tbc_config.json")

    loaded_from = None
    for p in config_paths:
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    file_cfg = json.load(f)
                    config.update(file_cfg)
                    loaded_from = str(p)
                    break
            except Exception as e:
                print(f"⚠️  Warning: Could not read config from {p}: {e}")

    # Environment variables override config file
    if os.environ.get("TBC_BOT_ID"):
        config["bot_id"] = os.environ.get("TBC_BOT_ID")
    if os.environ.get("TBC_LOGIN_TOKEN"):
        config["login_token"] = os.environ.get("TBC_LOGIN_TOKEN")
    if os.environ.get("TBC_COMMANDS_DIR"):
        config["commands_dir"] = os.environ.get("TBC_COMMANDS_DIR")
    if os.environ.get("TBC_API_BASE_URL"):
        config["api_base_url"] = os.environ.get("TBC_API_BASE_URL")

    # Command line arguments override everything
    if args.bot_id:
        config["bot_id"] = args.bot_id
    if args.login_token:
        config["login_token"] = args.login_token
    if args.dir:
        config["commands_dir"] = args.dir

    return config, loaded_from


def get_headers_and_cookies(config):
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "origin": "https://telebotcreator.com",
        "referer": "https://telebotcreator.com/"
    }
    cookies = {
        "login_token": config["login_token"]
    }
    return headers, cookies


def fetch_online_commands(config):
    base_url = config.get("api_base_url", "https://api.telebotcreator.com/v2").rstrip("/")
    bot_id = config["bot_id"]
    list_url = f"{base_url}/bots/{bot_id}/commands"
    headers, cookies = get_headers_and_cookies(config)

    response = requests.get(list_url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        raise RuntimeError(f"API Request failed ({response.status_code}): {response.text}")

    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Server returned error: {data.get('msg', 'Unknown error')}")

    return data.get("commands", []), list_url


def cmd_list(config):
    print("⌛ Fetching command list from Telebotcreator...")
    try:
        commands, _ = fetch_online_commands(config)
    except Exception as e:
        print(f"❌ Failed to fetch commands: {e}")
        return 1

    print(f"\n📋 Online Commands ({len(commands)} found) for Bot ID: {config['bot_id']}")
    print("-" * 75)
    print(f"{'Command Name':<25} | {'ID':<26} | {'Pinned':<7} | {'Admin Only'}")
    print("-" * 75)

    for cmd in sorted(commands, key=lambda x: x.get("command", "")):
        name = cmd.get("command", "<unknown>")
        cid = cmd.get("_id", "<no id>")
        pinned = "Yes" if cmd.get("pinned") else "No"
        admin = "Yes" if cmd.get("admin_only") else "No"
        print(f"{name:<25} | {cid:<26} | {pinned:<7} | {admin}")

    print("-" * 75)
    return 0


def cmd_pull(config, target_dir):
    print(f"⌛ Pulling commands from Telebotcreator into '{target_dir}/'...")
    try:
        commands, _ = fetch_online_commands(config)
    except Exception as e:
        print(f"❌ Failed to fetch commands: {e}")
        return 1

    os.makedirs(target_dir, exist_ok=True)
    pulled = 0

    for cmd in commands:
        cmd_name = cmd.get("command", "unnamed")
        code = cmd.get("code", "")
        # Sanitize filename
        safe_filename = re.sub(r'[\\/*?:"<>|]', '_', cmd_name)
        if safe_filename.startswith("/"):
            safe_filename = safe_filename.lstrip("/")
        if not safe_filename:
            safe_filename = "root"
        
        file_name = f"{safe_filename}.py"
        file_path = os.path.join(target_dir, file_name)

        # Ensure header metadata is present
        if not re.search(r'#\s*Command:\s*' + re.escape(cmd_name), code):
            header = f"# Command: {cmd_name}\n\n"
            code = header + code

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"  📥 Saved '{cmd_name}' -> {file_path}")
        pulled += 1

    print(f"\n✅ Pulled {pulled} commands to '{target_dir}'.")
    return 0


def cmd_init():
    template = {
        "bot_id": "YOUR_BOT_ID_HERE",
        "login_token": "YOUR_LOGIN_TOKEN_HERE",
        "commands_dir": "commands",
        "api_base_url": "https://api.telebotcreator.com/v2"
    }
    target = Path.cwd() / "tbc_config.json"
    if target.exists():
        print(f"⚠️  Config file already exists at {target}")
        return 1

    with open(target, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2)

    print(f"✅ Created starter configuration: {target}")
    print("👉 Edit this file with your bot_id and login_token.")
    return 0


def extract_command_name(file_path, code_content):
    match = re.search(r'#\s*Command:\s*(\S+)', code_content)
    if match:
        return match.group(1).strip()
    return os.path.splitext(os.path.basename(file_path))[0]


def sync_commands(config, single_file=None, dry_run=False):
    base_url = config.get("api_base_url", "https://api.telebotcreator.com/v2").rstrip("/")
    bot_id = config["bot_id"]
    headers, cookies = get_headers_and_cookies(config)

    print("⚡ TELEBOTCREATOR WORKSPACE SYNC")
    print("========================================")
    if dry_run:
        print("🔍 RUNNING IN DRY-RUN MODE (No changes will be applied)")

    # 1. Fetch online commands
    try:
        online_commands, list_url = fetch_online_commands(config)
    except Exception as e:
        print(f"❌ {e}")
        return 1

    print(f"👥 Found {len(online_commands)} commands online for bot {bot_id}.")
    online_map = {cmd["command"]: cmd for cmd in online_commands}

    # 2. Determine files to sync
    files_to_sync = []
    if single_file:
        p = Path(single_file)
        if not p.is_file():
            print(f"❌ File not found: {single_file}")
            return 1
        files_to_sync.append(p)
    else:
        commands_dir = Path(config.get("commands_dir", "commands"))
        if not commands_dir.exists():
            print(f"❌ Commands directory not found: {commands_dir}")
            return 1
        files_to_sync = sorted(list(commands_dir.glob("*.py")))

    print(f"📂 Processing {len(files_to_sync)} local file(s)...")
    print("========================================\n")

    success_count = 0
    fail_count = 0

    for file_path in files_to_sync:
        file_name = file_path.name
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            print(f"⚠️  [Failed] Could not read {file_name}: {e}")
            fail_count += 1
            continue

        command_name = extract_command_name(file_path, code_content)
        online_cmd = online_map.get(command_name)

        if not online_cmd:
            # CREATE Command
            print(f"➕ [Create] '{command_name}' (File: {file_name})")
            if dry_run:
                print("  └─ [Dry Run] Would POST new command to TBC")
                success_count += 1
                continue

            create_url = f"{base_url}/bots/{bot_id}/commands"
            payload = {"command": command_name, "code": ""}
            try:
                res = requests.post(create_url, headers=headers, cookies=cookies, json=payload)
                if res.status_code == 200 and res.json().get("ok"):
                    print("  └─ Created command online ✅")
                    # Refresh map
                    res_refresh = requests.get(list_url, headers=headers, cookies=cookies)
                    if res_refresh.status_code == 200:
                        online_map = {cmd["command"]: cmd for cmd in res_refresh.json().get("commands", [])}
                        online_cmd = online_map.get(command_name)
                else:
                    print(f"  └─ ❌ Creation failed: {res.text}")
                    fail_count += 1
                    continue
            except Exception as e:
                print(f"  └─ ❌ Connection error during creation: {e}")
                fail_count += 1
                continue

        # UPDATE Code Content
        if online_cmd:
            cmd_id = online_cmd["_id"]
            b64_cmd_name = base64.b64encode(command_name.encode()).decode().replace("=", "")
            update_url = f"{base_url}/bots/{bot_id}/commands/{b64_cmd_name}"

            payload = {
                "_id": cmd_id,
                "bot": bot_id,
                "command": command_name,
                "code": code_content,
                "created_at": online_cmd.get("created_at"),
                "pinned": online_cmd.get("pinned", False),
                "admin_only": online_cmd.get("admin_only", False)
            }

            print(f"⬆️  [Update] Uploading code for '{command_name}' (ID: {cmd_id})...")
            if dry_run:
                print(f"  └─ [Dry Run] Would PUT code ({len(code_content)} chars)")
                success_count += 1
                continue

            try:
                res = requests.put(update_url, headers=headers, cookies=cookies, json=payload)
                if res.status_code == 200:
                    print("  └─ Synchronized successfully! ✅")
                    success_count += 1
                else:
                    print(f"  └─ ❌ Upload failed ({res.status_code}): {res.text}")
                    fail_count += 1
            except Exception as e:
                print(f"  └─ ❌ Connection error during upload: {e}")
                fail_count += 1

    print("\n========================================")
    print("🏁 SYNC PROCESS COMPLETE")
    print(f"  🎉 Successful : {success_count}")
    print(f"  ⚠️  Failed     : {fail_count}")
    print(f"  📦 Total      : {success_count + fail_count}")
    print("========================================")
    return 0 if fail_count == 0 else 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="⚡ Telebotcreator (TBC) Workspace Synchronization Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  sync_tbc.py                       # Sync all files in commands/
  sync_tbc.py --file commands/.env.py # Sync a single file
  sync_tbc.py --list                # List all online commands
  sync_tbc.py --pull                # Pull online commands to commands/
  sync_tbc.py --dry-run             # Check status without modifying
  sync_tbc.py --init                # Generate starter tbc_config.json
"""
    )
    parser.add_argument("--bot-id", help="Telebotcreator Bot ID (overrides config)")
    parser.add_argument("--login-token", help="Telebotcreator login_token JWT cookie (overrides config)")
    parser.add_argument("--config", "-c", help="Path to custom JSON config file")
    parser.add_argument("--dir", "-d", help="Directory containing command files (default: 'commands')")
    parser.add_argument("--file", "-f", help="Specific command file to sync")
    parser.add_argument("--list", "-l", action="store_true", help="List all commands registered online")
    parser.add_argument("--pull", "-p", action="store_true", help="Pull online commands into the local commands directory")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Simulate synchronization without making changes")
    parser.add_argument("--init", action="store_true", help="Generate a starter tbc_config.json in current directory")

    args = parser.parse_args()

    if args.init:
        sys.exit(cmd_init())

    config, loaded_from = load_config(args)

    if not config["bot_id"] or not config["login_token"]:
        print("❌ Error: Both 'bot_id' and 'login_token' are required.")
        print("💡 You can provide them via:")
        print("   1. A local 'tbc_config.json' file (run 'sync_tbc.py --init')")
        print("   2. Global config '~/.gemini/config/tbc_config.json'")
        print("   3. Environment variables TBC_BOT_ID and TBC_LOGIN_TOKEN")
        print("   4. CLI flags --bot-id and --login-token")
        sys.exit(1)

    if loaded_from and not args.list:
        print(f"⚙️  Using configuration from: {loaded_from}")

    if args.list:
        sys.exit(cmd_list(config))
    elif args.pull:
        target_dir = args.dir or config.get("commands_dir", "commands")
        sys.exit(cmd_pull(config, target_dir))
    else:
        sys.exit(sync_commands(config, single_file=args.file, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
