import requests
import json

BASE = "https://opendataapi.pmc.gov.in/dataset-files"

target_dataset_id = 382

for page in range(33):
    params = {
        "page": page,
        "size": 10
    }

    r = requests.get(BASE, params=params, timeout=30)
    data = r.json()["data"]

    print(f"Checking page {page + 1}/33...")

    for file in data["content"]:
        if file["datasetId"] == target_dataset_id:
            print("\n" + "=" * 60)
            print("FOUND DATASET 382")
            print("=" * 60)
            print(json.dumps(file, indent=2))

            # Stop immediately
            raise SystemExit

print("\nDataset 382 was not found.")