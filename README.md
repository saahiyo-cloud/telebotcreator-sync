# Telebotcreator Sync

A simple tool to write your [Telebotcreator (TBC)](https://telebotcreator.com) Telegram bot code on your computer (in VS Code or any editor) and sync it directly to your bot.

---

## Why use this?

Normally, you have to write and edit your bot code inside the Telebotcreator browser window. 

With this tool, you can:
- Write your code locally in **VS Code**, **Cursor**, or **Notepad** with proper syntax highlighting and auto-save.
- Sync all your commands to Telebotcreator with a single command (`python scripts/sync_tbc.py`).
- Download (pull) commands already on your bot to your computer.
- Preview changes before applying them with `--dry-run`.
- Back up your bot code to GitHub.

---

## 3-Step Quick Start

### 1. Download & Install
Open your terminal and run:
```bash
git clone https://github.com/saahiyo-cloud/telebotcreator-sync.git
cd telebotcreator-sync
pip install requests
```

### 2. Create your config file
Run:
```bash
python scripts/sync_tbc.py --init
```
This creates a file named `tbc_config.json`. Open it and fill in your details:
```json
{
  "bot_id": "12345678",
  "login_token": "your_token_here",
  "commands_dir": "commands"
}
```

### 3. Sync your code!
Put your `.py` files inside the `commands/` folder, then run:
```bash
python scripts/sync_tbc.py
```
Done! Your commands are now live on Telebotcreator.

---

## How to get your Bot ID and Token

1. Go to [telebotcreator.com](https://telebotcreator.com/) and log into your account.
2. Click on your bot. Look at the web browser URL:
   `https://telebotcreator.com/bots/12345678/commands` -> Your Bot ID is **12345678**.
3. Press `F12` on your keyboard (or right-click anywhere and click **Inspect**).
4. Go to **Application** (or **Storage**) -> **Cookies** -> `https://telebotcreator.com`.
5. Copy the value of `login_token` and paste it into `tbc_config.json`.

---

## Cheat Sheet

| What you want to do | Command to run |
| :--- | :--- |
| **Upload all commands** | `python scripts/sync_tbc.py` |
| **Upload only one file** | `python scripts/sync_tbc.py --file commands/start.py` |
| **Check what would change without touching bot** | `python scripts/sync_tbc.py --dry-run` |
| **See list of online commands** | `python scripts/sync_tbc.py --list` |
| **Download online commands to your PC** | `python scripts/sync_tbc.py --pull` |

---

## How to Name Your Commands

Put `# Command: <name>` on the first line of your Python file:

```python
# Command: /start

def main():
    bot.send_message(message.chat.id, "Hello! Welcome to the bot.")
```

If you don't add this comment, the tool will just use the file's name (for example, `start.py` becomes `start`).

---

## Using with Google Antigravity AI

If you use the Google Antigravity IDE, this repo is already structured as an AI skill.

You can ask the AI in plain English:
- *"Upload my commands to Telebotcreator"*
- *"Show me my online bot commands"*
- *"Pull my bot commands down to this folder"*

---

## License

[MIT License](LICENSE) — free to use and modify for your own projects!
