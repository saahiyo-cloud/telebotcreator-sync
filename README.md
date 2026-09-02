# Telebotcreator Sync (`telebotcreator-sync`)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-green.svg)](https://github.com/saahiyo-cloud/telebotcreator-sync)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/saahiyo-cloud/telebotcreator-sync/pulls)

A developer synchronization utility and **Google Antigravity Skill** for [Telebotcreator (TBC)](https://telebotcreator.com).

Develop Telegram bot code locally in your IDE (VS Code, Cursor, Antigravity, PyCharm) with autocompletion, Git version control, and linter support, then synchronize changes directly to Telebotcreator via the API.

---

## Features

- **Bidirectional Synchronization**:
  - **Push / Sync**: Upload local `.py` command files to your Telebotcreator bot.
  - **Pull / Export**: Download online bot commands into your local directory.
- **Targeted Updates**: Sync all commands at once or target a single command file with `--file`.
- **Dry-Run Simulation**: Preview changes safely with `--dry-run` before applying them to your live bot.
- **Command Inspector**: List all online commands with IDs, pinned status, and admin restrictions.
- **Antigravity Skill Integration**: Native skill definition for Google Antigravity IDE.
- **Multi-Tier Configuration**: Configure via CLI flags, environment variables, local workspace JSON, or global system-wide config.
- **Automatic Metadata Parsing**: Extracts command names from Python file annotations (`# Command: /start` or `# Command: .env`).

---

## Quick Start

### 1. Installation

Clone this repository:
```bash
git clone https://github.com/saahiyo-cloud/telebotcreator-sync.git
cd telebotcreator-sync
```

Install requirements:
```bash
pip install requests
```

### 2. Initialize Configuration

Generate a starter configuration file in your project directory:
```bash
python scripts/sync_tbc.py --init
```

This creates `tbc_config.json`:
```json
{
  "bot_id": "YOUR_BOT_ID",
  "login_token": "YOUR_LOGIN_TOKEN_JWT",
  "commands_dir": "commands",
  "api_base_url": "https://api.telebotcreator.com/v2"
}
```

---

## How to Get Your Telebotcreator Credentials

1. Open [telebotcreator.com](https://telebotcreator.com/) and log in.
2. Select your bot. The **Bot ID** is the number in the browser URL:
   `https://telebotcreator.com/bots/29288962/commands` -> Bot ID: `29288962`
3. Press `F12` (or Right-Click -> **Inspect**) to open Developer Tools.
4. Navigate to **Application** (or **Storage**) -> **Cookies** -> `https://telebotcreator.com`.
5. Copy the value of the `login_token` cookie and paste it into `tbc_config.json`.

---

## CLI Usage

### Full Workspace Sync
Uploads all Python files from your `commands/` directory:
```bash
python scripts/sync_tbc.py
```

### Single Command Sync
Deploy only the command you just modified:
```bash
python scripts/sync_tbc.py --file commands/start.py
```

### Dry Run (Preview Changes)
Simulate synchronization without making actual API modifications:
```bash
python scripts/sync_tbc.py --dry-run
```

### List Online Commands
Inspect all commands currently active on your bot:
```bash
python scripts/sync_tbc.py --list
```

### Pull / Export Online Commands
Download all commands from Telebotcreator into your local `commands/` directory:
```bash
python scripts/sync_tbc.py --pull
```

---

## Using with Google Antigravity

You can install this repository as a global skill for the **Google Antigravity IDE** so that the agent can manage your bot commands when prompted.

### Global Installation:
Copy the skill folder into your Antigravity global configuration root:
```powershell
# Windows
mkdir "$env:USERPROFILE\.gemini\config\skills\tbc-sync"
Copy-Item -Recurse ./* "$env:USERPROFILE\.gemini\config\skills\tbc-sync\"
```

### Workspace Installation:
Place the skill into your project's `.agents/skills/tbc-sync/` folder.

Once installed, prompt the agent:
> *"Sync my local commands to Telebotcreator."*
> *"Update the start command online."*
> *"Check what commands are currently deployed on my bot."*

---

## Command Annotation Syntax

In your Python command files, specify the bot command name in the first comment line:

```python
# Command: /start

def handle_start(bot, message):
    bot.send_message(message.chat.id, "Welcome to my bot!")
```

If the `# Command:` header is omitted, the filename (without `.py`) is used automatically as the command name.

---

## Configuration Hierarchy

Credentials and settings are resolved in this priority order:
1. **CLI Flags**: `--bot-id`, `--login-token`, `--dir`, `--config`
2. **Environment Variables**: `TBC_BOT_ID`, `TBC_LOGIN_TOKEN`, `TBC_COMMANDS_DIR`
3. **Local Workspace Config**: `./tbc_config.json`
4. **Global System Config**: `~/.gemini/config/tbc_config.json`

---

## Security Best Practice

Never commit your `tbc_config.json` or `login_token` to public repositories. Keep `tbc_config.json` listed in your `.gitignore`.

---

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/saahiyo-cloud/telebotcreator-sync/issues).

---

## License

This project is licensed under the [MIT License](LICENSE).
