import requests
import json

BASE = "https://opendataapi.pmc.gov.in/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

DATASET_ID = 335


def print_response(response):
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Length:", len(response.content))

    print("\nHeaders:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")

    print("\nResponse:")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception:
        print(response.text[:10000])


# -------------------------------------------------------------------
# 1. Get dataset metadata
# -------------------------------------------------------------------

print("=" * 80)
print(f"GET DATASET {DATASET_ID}")
print("=" * 80)

try:
    response = requests.get(
        BASE + f"datasets/{DATASET_ID}",
        headers=headers,
        timeout=20
    )

    print_response(response)

except Exception as e:
    print("ERROR:", e)


# -------------------------------------------------------------------
# 2. Get files belonging to the dataset
# -------------------------------------------------------------------

print()
print("=" * 80)
print(f"GET DATASET FILES FOR {DATASET_ID}")
print("=" * 80)

try:
    response = requests.get(
        BASE + "dataset-files",
        params={
            "datasetId": DATASET_ID
        },
        headers=headers,
        timeout=20
    )

    print("Requested URL:", response.url)
    print_response(response)

except Exception as e:
    print("ERROR:", e)


# -------------------------------------------------------------------
# 3. Test the frontend's download-purpose endpoint
# -------------------------------------------------------------------

print()
print("=" * 80)
print(f"POST SAVE DOWNLOAD PURPOSE FOR {DATASET_ID}")
print("=" * 80)

url = BASE + f"dataset-files/{DATASET_ID}/save-download-purpose"

payload = {}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20
    )

    print("Requested URL:", response.url)
    print_response(response)

except Exception as e:
    print("ERROR:", e)