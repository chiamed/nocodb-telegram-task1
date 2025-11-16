from dotenv import load_dotenv
import os
import json
import requests

# SWAGGER docs prefix
DATA_PREFIX = "api/v2/tables"

# load environment variables
load_dotenv()

auth_token = os.getenv("nocodb_auth_token")
base_url = os.getenv("nocodb_url") 
table_id = os.getenv("nocodb_table_id")
json_path = os.getenv("nocodb_upload_file_path")

# construct insert URL
insert_url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

# authenticate
headers = {
    "xc-token": auth_token,
    "accept": "application/json",
    "Content-Type": "application/json"
}

# read JSON file
with open(json_path, "r", encoding="utf-8") as f:
    records = json.load(f)

# upload rows
for record in records:
    print("Uploading:", record)
    r = requests.post(insert_url, headers=headers, json=record)

    if r.status_code >= 400:
        print("ERROR:", r.text)
        raise Exception("Upload failed")

print("Upload completed!")

