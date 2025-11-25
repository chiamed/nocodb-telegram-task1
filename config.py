import os
from dotenv import load_dotenv

# NocoDB API prefix
DATA_PREFIX = "api/v2/tables"

# Load environment variables
load_dotenv()

auth_token = os.getenv("nocodb_auth_token")
base_url = os.getenv("nocodb_url")
bot_token = os.getenv("telegram_bot_token")
table_odg = os.getenv("table_odg")
table_users = os.getenv("table_users")
table_areas = os.getenv("table_areas")
table_departments = os.getenv("table_departments")