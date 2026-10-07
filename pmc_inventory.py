import requests
import json
import csv
import time

BASE = "https://opendataapi.pmc.gov.in"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

all_datasets = []

page = 0
size = 100

while True:

    url = f"{BASE}/datasets?page={page}&size={size}"

    print(f"Fetching page {page}...")

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    data = result["data"]

    content = data["content"]

    print(f"  Records: {len(content)}")

    all_datasets.extend(content)

    if data["last"]:
        break

    page += 1
    time.sleep(0.5)


print()
print("=" * 70)
print("INVENTORY COMPLETE")
print("=" * 70)

print("Datasets:", len(all_datasets))


# --------------------------------------------------
# Save complete JSON
# --------------------------------------------------

with open(
    "pmc_datasets.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        all_datasets,
        f,
        indent=2,
        ensure_ascii=False
    )


# --------------------------------------------------
# Flatten dataset + files
# --------------------------------------------------

rows = []

for dataset in all_datasets:

    files = dataset.get("datasetFile") or [None]

    for file in files:

        rows.append({
            "datasetId": dataset.get("datasetId"),
            "datasetTitle": dataset.get("datasetTitle"),
            "metaData": dataset.get("metaData"),
            "createdDate": dataset.get("createdDate"),
            "modifiedDate": dataset.get("modifiedDate"),
            "departmentId": dataset.get("departmentId"),
            "categoryId": dataset.get("categoryId"),
            "tags": dataset.get("tags"),
            "downloadCount": dataset.get("downloadCount"),

            "datasetFileId": (
                file.get("fileId")
                if file else None
            ),

            "filePath": (
                file.get("filePath")
                if file else None
            ),

            "format": (
                file.get("format")
                if file else None
            ),

            "fileSize": (
                file.get("fileSize")
                if file else None
            ),
        })


with open(
    "pmc_inventory.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)


print("Dataset records:", len(all_datasets))
print("File records:", len(rows))

print()
print("Saved:")
print("  pmc_datasets.json")
print("  pmc_inventory.csv")