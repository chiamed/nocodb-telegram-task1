import json
from time import sleep
import requests
from config import DATA_PREFIX, auth_token, base_url, table_areas, table_departments, table_users

# Authenticate
headers = {
    "xc-token": auth_token,
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Normalize values for comparison (lowercase and without spaces)
def normalize(val):
    if val is None:
        return ""
    if not isinstance(val, str):
        val = str(val)
    return val.strip().lower()

# Return a set of normalized existing values for key_field
def get_existing_keys(table_id, key_field):
    existing = set()
    offset = 0
    PAGE_LIMIT = 200

    while True:
        url = f"{base_url}/{DATA_PREFIX}/{table_id}/records?limit={PAGE_LIMIT}&offset={offset}"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, dict) and "list" in data:
            records = data["list"]
            is_last = data.get("pageInfo", {}).get("isLastPage", False)
        elif isinstance(data, list):
            records = data
            is_last = len(records) < PAGE_LIMIT
        else:
            raise RuntimeError("Unexpected GET response shape")

        for rec in records:
            raw = rec.get(key_field)
            norm = normalize(raw)
            if norm:
                existing.add(norm)

        if is_last:
            break

        offset += PAGE_LIMIT
        sleep(0.03)

    return existing


# Upload only missing records and return mapping key -> recordId
def upload_and_build_map(json_path, table_id, key_field):
    url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

    #print(f"\nImporting {json_path} into table {table_id}")

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    existing = get_existing_keys(table_id, key_field)
    id_map = {}

    for item in items:
        key = item[key_field]
        norm = normalize(key)

        if norm in existing:
            # fetch ID of already existing record
            q = f'?where=({key_field},eq,{key})'
            r = requests.get(f"{url}{q}", headers=headers)
            rec = r.json()["list"][0]
            id_map[key] = rec["Id"]
            continue

        # insert if missing
        r = requests.post(url, headers=headers, json=item)
        record_id = r.json()["Id"]
        id_map[key] = record_id
        existing.add(norm)

    return id_map


def upload_users(json_path, table_id, areas_map, departments_map):
    url = f"{base_url}/{DATA_PREFIX}/{table_id}/records"

    existing = get_existing_keys(table_id, "Personal Email")

    with open(json_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    for u in users:
        email = normalize(u.get("Personal Email"))
        if email in existing:
            continue

        # Map relations
        if u.get("Department"):
            u["departments_id"] = departments_map.get(u["Department"])

        if u.get("Area"):
            area_key = u["Area"].split(" - ")[0]
            u["areas_id"] = areas_map.get(area_key)

        # Upload user
        r = requests.post(url, headers=headers, json=u)
        if r.status_code >= 400:
            print("ERROR:", r.text, "\nUser:", u)
            raise Exception("User upload failed")
        #print("Users imported successfully!\n")

        existing.add(email)
        sleep(0.03)

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
    json_path="data/users.json",
    table_id=table_users,
    areas_map=areas_map,
    departments_map=departments_map
)

print("ALL IMPORTS COMPLETED SUCCESSFULLY!")