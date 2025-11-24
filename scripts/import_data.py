import os
import json
import requests
from config import DATA_PREFIX, auth_token, base_url

# Authenticate
headers = {
    "xc-token": auth_token,
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Table IDs from .env
table_areas = os.getenv("table_areas")
table_departments = os.getenv("table_departments")
table_users = os.getenv("table_users")


def upload_and_build_map(json_path, table_id, key_field):
    url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

    print(f"\nImporting {json_path} into table {table_id}")

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    id_map = {}

    for item in items:
        r = requests.post(url, headers=headers, json=item)
        if r.status_code >= 400:
            print("ERROR:", r.text)
            raise Exception(f"Upload failed for {json_path}")

        record_id = r.json().get("Id")
        id_map[item[key_field]] = record_id

    print(f"Completed import of {json_path}")
    return id_map


def upload_users(users_json, table_id, areas_map, departments_map):
    url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

    print(f"\nImporting users from {users_json}")

    with open(users_json, "r", encoding="utf-8") as f:
        users = json.load(f)

    for u in users:
        # Map Department
        if "Department" in u and u["Department"]:
            dep_key = u["Department"]
            u["departments_id"] = departments_map.get(dep_key)

        # Map Area
        if "Area" in u and u["Area"]:
            area_key = u["Area"].split(" - ")[0]
            u["areas_id"] = areas_map.get(area_key)

        # Upload user
        r = requests.post(url, headers=headers, json=u)
        if r.status_code >= 400:
            print("ERROR:", r.text)
            print("User:", u)
            raise Exception("User upload failed")
        print("Users imported successfully!\n")


# 1. Import AREAS
areas_map = upload_and_build_map(
    json_path="data/areas.json",
    table_id=table_areas,
    key_field="Tag"
)

# 2. Import DEPARTMENTS
departments_map = upload_and_build_map(
    json_path="data/departments.json",
    table_id=table_departments,
    key_field="Name"
)

# 3. Import USERS with mapped relations
upload_users(
    users_json="data/users.json",
    table_id=table_users,
    areas_map=areas_map,
    departments_map=departments_map
)

print("ALL IMPORTS COMPLETED SUCCESSFULLY!")