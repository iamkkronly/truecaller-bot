# Truecaller Telegram Bot

This is a Telegram bot that allows you to look up phone number information using the `truecallerjs` library.

## Prerequisites

*   A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
*   A Truecaller account (phone number)
*   A [Render](https://render.com) account (for deployment)

## Setup

1.  **Clone this repository** (or fork it).
2.  **Edit `bot.py`**:
    *   Open `bot.py` in a text editor.
    *   Find the `BOT_TOKEN` variable and replace `"7801237842:AAFw-..."` with your actual Bot Token.
    *   Find the `ADMIN_ID` variable and replace `"123456789"` with your Telegram User ID. You can find your User ID by messaging [@userinfobot](https://t.me/userinfobot) on Telegram.

    ```python
    # Example
    BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ"
    ADMIN_ID = "987654321"
    ```

## Deploy on Render (Free Web Service)

Since `truecallerjs` requires a Node.js environment and the bot is written in Python, we need a custom environment. This repository includes a `Dockerfile` to handle this.

### 1. Deploy to Render

1.  Push your changes (including the modified `bot.py`) to GitHub/GitLab.
2.  Log in to your [Render Dashboard](https://dashboard.render.com).
3.  Click **New +** and select **Web Service**.
4.  Connect your repository.
5.  In the configuration page:
    *   **Name**: Give your service a name.
    *   **Runtime**: Select **Docker**.
    *   **Instance Type**: Select **Free**.
6.  Click **Create Web Service**.

## Login to Truecaller (Important!)

After the deployment finishes, the bot will start, but it won't be able to fetch data until you log in to Truecaller on the server.

1.  Go to your Render Dashboard and open your service.
2.  Click on the **Shell** tab (this connects you to the running container).
3.  Run the following command:
    ```bash
    truecallerjs login
    ```
4.  Follow the interactive prompts:
    *   Type `Y` to login.
    *   Enter your phone number (e.g., `+1234567890`).
    *   Enter the OTP received on your phone.

Once logged in, the bot is ready to use!

**Note:** On Render's Free tier, the filesystem is ephemeral. This means if the service is restarted or redeployed, the login session (stored in `~/.config/truecallerjs/`) might be lost, and you may need to repeat the login step.

## Usage

1.  Open your bot in Telegram.
2.  Send `/start` to see the welcome message.
3.  Send a phone number (e.g., `+19876543210`) to look it up.
    *   **Only the Admin (configured in `bot.py`) can use the bot.** Other users will receive an "Unauthorized" message.

## Troubleshooting

*   **"Error: The bot server is not logged in to Truecaller"**: This means the `truecallerjs login` step was not completed or the session was lost. Go to the Render Shell and login again.
*   **"Unauthorized access"**: Ensure your `ADMIN_ID` in `bot.py` matches your Telegram User ID.
