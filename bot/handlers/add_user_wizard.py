from telegram import Update
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import requests
from config import base_url, DATA_PREFIX, table_users, auth_token

(
    NAME,
    SURNAME,
    PERSONAL_EMAIL,
    UNIVERSITY_EMAIL,
    PHONE,
    TELEGRAM_USERNAME,
    ENTRY,
    #DEPARTMENT,
    #AREA,
    SEX,
    BIRTH,
    CONFIRM
) = range(10)

async def adduser_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter the user's first name.")
    return NAME

async def get_name(update, context):
    context.user_data["Name"] = update.message.text
    await update.message.reply_text("Now enter the last name.")
    return SURNAME

async def get_surname(update, context):
    context.user_data["Surname"] = update.message.text
    await update.message.reply_text("Enter the personal email.")
    return PERSONAL_EMAIL

async def get_personal_email(update, context):
    context.user_data["Personal Email"] = update.message.text
    await update.message.reply_text("Enter the university email.")
    return UNIVERSITY_EMAIL

async def get_university_email(update, context):
    context.user_data["University Email"] = update.message.text
    await update.message.reply_text("Enter the phone number.")
    return PHONE

async def get_phone(update, context):
    context.user_data["Phone Number"] = update.message.text
    await update.message.reply_text("Enter the Telegram username (e.g., @username).")
    return TELEGRAM_USERNAME

async def get_telegram(update, context):
    context.user_data["Telegram Username"] = update.message.text
    await update.message.reply_text("Enter the team entry date.")
    return ENTRY

async def get_entry_date(update, context):
    context.user_data["Entry Date"] = update.message.text
    await update.message.reply_text("Enter the sex (Male/Female).")
    return SEX

async def get_sex(update, context):
    context.user_data["Sex"] = update.message.text
    await update.message.reply_text("Enter the date of birth (YYYY-MM-DD).")
    return BIRTH

async def get_birth(update, context):
    context.user_data["Date of Birth"] = update.message.text

    summary = "\n".join([f"*{k}:* {v}" for k, v in context.user_data.items()])

    await update.message.reply_text(
        f"Review the entered data:\n\n{summary}\n\nDo you confirm? (yes/no)",
        parse_mode="Markdown")
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.lower()

    if answer not in ["yes", "y", "si", "sì"]:
        await update.message.reply_text("Operation canceled.")
        return ConversationHandler.END

    url = f"{base_url}/{DATA_PREFIX}/{table_users}/records"
    headers = {"xc-token": auth_token, "Content-Type": "application/json"}

    payload = {**context.user_data}
    r = requests.post(url, json=payload, headers=headers)

    if r.status_code >= 400:
        await update.message.reply_text("Error during insertion")
    else:
        await update.message.reply_text("User successfully added!")

    return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

add_user_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("adduser", adduser_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
        PERSONAL_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_personal_email)],
        UNIVERSITY_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_university_email)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        TELEGRAM_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram)],
        ENTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_entry_date)],
        #DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_department)],
        #AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_area)],
        SEX: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sex)],
        BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth)],
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)