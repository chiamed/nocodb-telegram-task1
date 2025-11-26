from telegram import Update
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
import requests

from config import (
    base_url, DATA_PREFIX, table_users, auth_token,
    table_departments, table_areas
)
from services.helpers import fetch_id_map, build_inline_keyboard
from services.validators import (
    is_valid_email, is_valid_phone, is_valid_username,
    is_valid_date, normalize_sex
)


(
    NAME,
    SURNAME,
    PERSONAL_EMAIL,
    UNIVERSITY_EMAIL,
    PHONE,
    TELEGRAM_USERNAME,
    DEPARTMENT,
    AREA,
    ENTRY,
    SEX,
    BIRTH,
    CONFIRM
) = range(12)

def build_summary(data):
    allowed_keys = [
        "Name",
        "Surname",
        "Personal Email",
        "University Email",
        "Phone Number",
        "Telegram Username",
        "Department",
        "Area",
        "Entry Date",
        "Sex",
        "Date of Birth",
    ]

    lines = []
    for key in allowed_keys:
        if key in data:
            lines.append(f"*{key}:* {data[key]}")

    return "\n".join(lines)

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
    email = update.message.text

    if not is_valid_email(email):
        await update.message.reply_text("Invalid email format. Try again.")
        return PERSONAL_EMAIL

    context.user_data["Personal Email"] = email
    await update.message.reply_text("Enter the university email.")
    return UNIVERSITY_EMAIL


async def get_university_email(update, context):
    email = update.message.text

    if not is_valid_email(email):
        await update.message.reply_text("Invalid email format. Try again.")
        return UNIVERSITY_EMAIL

    context.user_data["University Email"] = email
    await update.message.reply_text("Enter the phone number.")
    return PHONE

async def get_phone(update, context):
    phone = update.message.text

    if not is_valid_phone(phone):
        await update.message.reply_text("Invalid phone number. Use digits only. Try again.")
        return PHONE

    context.user_data["Phone Number"] = phone
    await update.message.reply_text("Enter the Telegram username (e.g., @username).")
    return TELEGRAM_USERNAME

async def get_telegram(update, context):
    username = update.message.text.strip()

    # Validate the Telegram username
    if not is_valid_username(username):
        await update.message.reply_text(
            "Invalid Telegram username.\n"
            "It must start with @ and contain 3-32 letters, numbers or underscores.\n"
            "Try again:"
        )
        return TELEGRAM_USERNAME

    # Save to context only if valid
    context.user_data["Telegram Username"] = username

    # Fetch departments
    departments = fetch_id_map(table_departments, "Name")
    context.user_data["departments_map"] = departments

    keyboard = build_inline_keyboard(list(departments.keys()), "dept")

    await update.message.reply_text(
        "Select the department:",
        reply_markup=keyboard
    )

    return DEPARTMENT


async def get_department(update, context):
    q = update.callback_query
    await q.answer()

    selected = q.data.split("dept:")[1]
    context.user_data["Department"] = selected
    context.user_data["departments_id"] = context.user_data["departments_map"][selected]

    await q.edit_message_text(f"Department selected: *{selected}*", parse_mode="Markdown")

    # fetch areas
    areas = fetch_id_map(table_areas, "Tag")
    context.user_data["areas_map"] = areas

    keyboard = build_inline_keyboard(list(areas.keys()), "area")
    await q.message.reply_text("Select the area:", reply_markup=keyboard)

    return AREA

async def get_area(update, context):
    q = update.callback_query
    await q.answer()

    selected = q.data.split("area:")[1]
    context.user_data["Area"] = selected
    context.user_data["areas_id"] = context.user_data["areas_map"][selected]


    await q.edit_message_text(f"Area selected: *{selected}*", parse_mode="Markdown")
    await q.message.reply_text("Enter the team entry date (YYYY-MM-DD).")
    return ENTRY

async def get_entry_date(update, context):
    date = update.message.text

    if not is_valid_date(date):
        await update.message.reply_text("Invalid date. Use YYYY-MM-DD.")
        return ENTRY

    context.user_data["Entry Date"] = date
    await update.message.reply_text("Enter the sex (Male/Female).")
    return SEX

async def get_sex(update, context):
    sex = normalize_sex(update.message.text)

    if sex is None:
        await update.message.reply_text("Invalid value. Use Male / Female.")
        return SEX

    context.user_data["Sex"] = sex
    await update.message.reply_text("Enter the date of birth (YYYY-MM-DD).")
    return BIRTH

async def get_birth(update, context):
    date = update.message.text

    if not is_valid_date(date):
        await update.message.reply_text("Invalid date. Use YYYY-MM-DD.")
        return BIRTH

    context.user_data["Date of Birth"] = date
    # Build safe summary (avoids sending giant dictionaries)
    summary = build_summary(context.user_data)

    # Ask for confirmation
    await update.message.reply_text(
        f"Review the entered data:\n\n{summary}\n\nDo you confirm? (yes/no)",
        parse_mode="Markdown"
    )

    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.lower()

    if answer not in ["yes", "y", "si", "sì"]:
        await update.message.reply_text("Operation canceled.")
        return ConversationHandler.END

    url = f"{base_url}/{DATA_PREFIX}/{table_users}/records"
    headers = {"xc-token": auth_token, "Content-Type": "application/json"}

    payload = {
        "Name": context.user_data["Name"],
        "Surname": context.user_data["Surname"],
        "Personal Email": context.user_data["Personal Email"],
        "University Email": context.user_data["University Email"],
        "Phone Number": context.user_data["Phone Number"],
        "Telegram Username": context.user_data["Telegram Username"],
        "departments_id": context.user_data["departments_id"],
        "areas_id": context.user_data["areas_id"],
        "Entry Date": context.user_data["Entry Date"],
        "Sex": context.user_data["Sex"],
        "Date of Birth": context.user_data["Date of Birth"],
    }

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
        DEPARTMENT: [CallbackQueryHandler(get_department, pattern="^dept:")],
        AREA: [CallbackQueryHandler(get_area, pattern="^area:")],
        SEX: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sex)],
        BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth)],
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
