# Telebotcreator (TBC) Configuration & API Reference

This document provides complete details on configuring and working with the Telebotcreator Sync skill.

---

## 1. Configuration Keys

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `bot_id` | `string` | *(Required)* | Numerical ID of the Telebotcreator bot (found in the dashboard URL). |
| `login_token` | `string` | *(Required)* | JWT session token from the `login_token` cookie when logged into telebotcreator.com. |
| `commands_dir` | `string` | `"commands"` | Relative or absolute path to the directory where command Python files are stored. |
| `api_base_url` | `string` | `"https://api.telebotcreator.com/v2"` | API base endpoint for Telebotcreator v2. |

---

## 2. Environment Variables

Instead of storing credentials in a JSON file on disk, you can pass them as environment variables:

- `TBC_BOT_ID`: Sets the active bot ID.
- `TBC_LOGIN_TOKEN`: Sets the JWT login token.
- `TBC_COMMANDS_DIR`: Sets the default directory for command files.
- `TBC_API_BASE_URL`: Overrides the API base URL.

---

## 3. Telebotcreator REST API Endpoints

### Fetch Commands
- **Method**: `GET`
- **URL**: `https://api.telebotcreator.com/v2/bots/{bot_id}/commands`
- **Headers**:
  ```json
  {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": "https://telebotcreator.com",
    "referer": "https://telebotcreator.com/"
  }
  ```
- **Cookie**: `login_token={login_token}`

### Create Command
- **Method**: `POST`
- **URL**: `https://api.telebotcreator.com/v2/bots/{bot_id}/commands`
- **Body**:
  ```json
  {
    "command": "command_name",
    "code": ""
  }
  ```

### Update Command Code
- **Method**: `PUT`
- **URL**: `https://api.telebotcreator.com/v2/bots/{bot_id}/commands/{base64_encoded_command_name}`
  - Note: The command name is base64url encoded with padding (`=`) stripped.
- **Body**:
  ```json
  {
    "_id": "<command_id>",
    "bot": "<bot_id>",
    "command": "<command_name>",
    "code": "<full_python_source_code>",
    "created_at": "<timestamp>",
    "pinned": false,
    "admin_only": false
  }
  ```

---

## 4. How to Retrieve Your Login Token
1. Open [telebotcreator.com](https://telebotcreator.com/) and log into your account.
2. Open Browser Developer Tools (`F12` or right click -> Inspect).
3. Go to the **Application** (or **Storage**) tab -> **Cookies** -> `https://telebotcreator.com`.
4. Copy the value of the `login_token` cookie.
