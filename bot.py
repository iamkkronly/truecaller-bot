import telebot
import subprocess
import json
import os
import re

# Get BOT_TOKEN from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable not set.")
    print("Please set the BOT_TOKEN environment variable.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Handle /start and /help commands.
    """
    bot.reply_to(message, "Welcome! Send me a phone number to lookup using TruecallerJS.\n\n"
                          "Note: The server hosting this bot must be logged in to TruecallerJS.")

@bot.message_handler(func=lambda message: True)
def lookup_number(message):
    """
    Handle all other messages as phone numbers to lookup.
    """
    phone_number = message.text.strip()

    # Basic input validation
    # Allow digits, spaces, and optional leading +
    if not re.match(r'^\+?[\d\s]+$', phone_number):
        bot.reply_to(message, "Invalid phone number format. Please send a valid phone number (e.g., +1234567890).")
        return

    # Notify user that search is in progress
    msg = bot.reply_to(message, "Searching...")

    try:
        # Construct command: truecallerjs -s <number> --json
        command = ['truecallerjs', '-s', phone_number, '--json']

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = result.stderr.strip() or result.stdout.strip()
            if not error_message:
                error_message = "Unknown error occurred."

            # Check for common errors
            if "login" in error_message.lower():
                bot.edit_message_text(
                    "Error: The bot server is not logged in to Truecaller.\n"
                    "Please run `truecallerjs login` on the server.",
                    chat_id=message.chat.id,
                    message_id=msg.message_id
                )
            else:
                bot.edit_message_text(
                    f"Error: {error_message}",
                    chat_id=message.chat.id,
                    message_id=msg.message_id
                )
            return

        output = result.stdout.strip()

        if not output:
             bot.edit_message_text("Error: Received empty response from TruecallerJS.", chat_id=message.chat.id, message_id=msg.message_id)
             return

        try:
            data = json.loads(output)

            # Format the output
            response_text = f"**Truecaller Lookup Result:**\n\n"

            if isinstance(data, list) and len(data) > 0:
                data = data[0]

            # Basic Info
            name = data.get('name', 'N/A')
            alt_name = data.get('altName')
            gender = data.get('gender')
            score = data.get('score')

            response_text += f"**Name:** {name}\n"
            if alt_name:
                 response_text += f"**Alt Name:** {alt_name}\n"
            if gender:
                 response_text += f"**Gender:** {gender}\n"
            if score:
                 response_text += f"**Score:** {score}\n"

            # Phones
            phones = data.get('phones', [])
            if phones:
                response_text += "\n**Phones:**\n"
                for p in phones:
                    number = p.get('e164Format', p.get('number', 'N/A'))
                    carrier = p.get('carrier', 'N/A')
                    country = p.get('countryCode', 'N/A')
                    response_text += f"- `{number}` ({carrier}, {country})\n"

            # Addresses
            addresses = data.get('addresses', [])
            if addresses:
                response_text += "\n**Addresses:**\n"
                for a in addresses:
                    city = a.get('city', 'N/A')
                    country = a.get('countryCode', 'N/A')
                    response_text += f"- {city}, {country}\n"

            # Emails
            internet_addresses = data.get('internetAddresses', [])
            if internet_addresses:
                response_text += "\n**Internet/Email:**\n"
                for i in internet_addresses:
                    if i.get('service') == 'EMAIL':
                         response_text += f"- {i.get('id', 'N/A')}\n"
                    else:
                         response_text += f"- {i.get('service', 'N/A')}: {i.get('id', 'N/A')}\n"

            # Send the formatted message
            bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=msg.message_id, parse_mode='Markdown')

        except json.JSONDecodeError:
            # Fallback if JSON parsing fails but return code was 0
            bot.edit_message_text(f"Error parsing response. Raw output:\n{output[:1000]}", chat_id=message.chat.id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"An unexpected error occurred: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling()
