import json
import csv

INPUT_FILE = "pmc_datasets.json"
OUTPUT_FILE = "pmc_dataset_basic.csv"

# Load dataset inventory

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    datasets = json.load(f)

# Extract only required fields

rows = []

for dataset in datasets:

    rows.append({
        "datasetId": dataset.get("datasetId"),
        "datasetTitle": dataset.get("datasetTitle"),
        "metaData": dataset.get("metaData")
    })

# Save CSV

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "datasetId",
            "datasetTitle",
            "metaData"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

# Summary

print("=" * 60)
print("EXTRACTION COMPLETE")
print("=" * 60)

print("Datasets:", len(rows))
print("Saved:", OUTPUT_FILE)