import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from .handlers.add_user_wizard import add_user_conv_handler
from config import bot_token, DATA_PREFIX, table_odg, auth_token, base_url
from services.helpers import escape_markdown

"""
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "🦅 Welcome to the Eagle Racing Team Bot! \n\n"
            "I'm here to help you manage internal activities — "
            "from adding new users to checking the latest Ordini del Giorno.\n\n"
            "Type /help to see all available commands."
        ),
        parse_mode="Markdown"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
    "👋 Here I am to help you! These are the commands you can use:\n\n"
    "➡️ /start — Start the bot and get a quick introduction\n"
    "➡️ /odg — View the latest Ordini del Giorno\n"
    "➡️ /adduser — Begin the guided process to add a new user\n\n"
)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def odg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"{base_url}/{DATA_PREFIX}/{table_odg}/records"
    headers = {
        "xc-token": auth_token,
        "accept": "application/json"
    }

    r = requests.get(url, headers=headers)
    data = r.json().get("list", [])

    if not data:
        await update.message.reply_text("No ODG found.")
        return

    msg = "*Ordini del Giorno:*\n\n"

    for item in data:
        title = escape_markdown(item.get("Title", "Untitled"))
        date = escape_markdown(item.get("Date", "Date not available"))
        description = escape_markdown(item.get("Description", "No description"))
        activities = escape_markdown(item.get("Activities", "No activities"))

        msg += (
            f"*{title}*\n"
            f"Data: {date}\n"
            f"{description}\n\n"
            f"*Attività:*\n"
            f"{activities}\n\n"
        )

    await update.message.reply_text(msg, parse_mode="MarkdownV2")


def main():
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("odg", odg))
    app.add_handler(add_user_conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
