---
name: tbc-sync
description: >-
  Synchronize, pull, inspect, and manage Telebotcreator (TBC) bot commands between a local workspace and the Telebotcreator platform.
  Use this skill whenever the user asks to sync, upload, deploy, pull, list, or update Telegram bot commands on Telebotcreator.
---

# Telebotcreator Synchronization Skill (`tbc-sync`)

This skill enables synchronization of local Python command files with the Telebotcreator (TBC) platform via the TBC REST API.

## When to Use

Activate this skill when:
- Deploying or syncing local command code in `commands/` to a Telebotcreator bot.
- Syncing a single edited command file (e.g. `commands/start.py`).
- Pulling / exporting existing commands from Telebotcreator down to a local directory.
- Checking or listing all commands registered on a Telebotcreator bot.
- Testing or previewing command changes with a dry-run.

---

## Configuration

The sync utility resolves credentials and settings in the following order:

1. CLI Arguments: `--bot-id`, `--login-token`, `--dir`, `--config`
2. Environment Variables: `TBC_BOT_ID`, `TBC_LOGIN_TOKEN`, `TBC_COMMANDS_DIR`
3. Local Workspace Config: `./tbc_config.json`
4. Global Config: `~/.gemini/config/tbc_config.json`

### Configuration Format (`tbc_config.json`)
```json
{
  "bot_id": "YOUR_BOT_ID",
  "login_token": "YOUR_LOGIN_TOKEN_JWT",
  "commands_dir": "commands",
  "api_base_url": "https://api.telebotcreator.com/v2"
}
```

---

## Command Annotations

Every command file in `commands/` can include a metadata comment on line 1:
```python
# Command: /start
```
or
```python
# Command: .env
```
- If this header is present, the script uses that exact name when registering or updating the command on Telebotcreator.
- If omitted, the script falls back to the filename without the `.py` extension.

---

## Workflows & Commands

### 1. Sync All Commands (Full Workspace)
```powershell
python "scripts/sync_tbc.py"
```

### 2. Sync a Single Command File
```powershell
python "scripts/sync_tbc.py" --file commands/start.py
```

### 3. Dry-Run / Preview Changes
```powershell
python "scripts/sync_tbc.py" --dry-run
```

### 4. List All Online Bot Commands
```powershell
python "scripts/sync_tbc.py" --list
```

### 5. Pull Online Commands to Local Workspace
```powershell
python "scripts/sync_tbc.py" --pull
```

### 6. Initialize Config in a New Project
```powershell
python "scripts/sync_tbc.py" --init
```

---

## Reference & Troubleshooting
- [Configuration & API Reference](./references/configuration.md)
