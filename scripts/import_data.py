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

# authenticate
headers = {
    "xc-token": auth_token,
    "accept": "application/json",
    "Content-Type": "application/json"
}

# mapping: file json -> table_id
tables = {
    "data/areas.json": os.getenv("table_areas"),
    "data/departments.json": os.getenv("table_departments"),
    "data/users.json": os.getenv("table_users"),
}

def upload_json(json_path, table_id):
    url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

    print(f"\nImporting {json_path} into table {table_id}")

    # read JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # upload rows
    for record in records:
        print("Uploading:", record)
        r = requests.post(url, headers=headers, json=record)

        if r.status_code >= 400:
            print("ERROR:", r.text)
            raise Exception("Upload failed")

    print(f"Completed import of {json_path}\n")


# run imports in order
for json_path, table_id in tables.items():
    upload_json(json_path, table_id)

print("ALL IMPORTS COMPLETED SUCCESSFULLY!")


