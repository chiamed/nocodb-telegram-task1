import requests
from config import base_url, DATA_PREFIX, auth_token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Fetch a mapping of field values to IDs from a specific table
# This function sends a GET request to the NocoDB API and returns a dictionary
# where the keys are the values of the specified field and the values are the corresponding IDs
def fetch_id_map(table_name, field):
    url = f"{base_url}/{DATA_PREFIX}/{table_name}/records"
    headers = {"xc-token": auth_token}

    r = requests.get(url, headers=headers).json()
    return {item[field]: item["Id"] for item in r["list"]}

# Build an inline keyboard for Telegram bots
# This function creates a keyboard with buttons, where each button has a label
# and a callback data value prefixed with the specified string
def build_inline_keyboard(options, prefix):
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"{prefix}:{opt}")]
        for opt in options
    ]
    return InlineKeyboardMarkup(buttons)

# Escape special Markdown characters in a string
# This function ensures that special characters used in Markdown formatting
# are escaped to prevent unintended formatting in Telegram messages
def escape_markdown(text: str) -> str:
    if not text:
        return ""
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return "".join("\\" + c if c in escape_chars else c for c in text)

