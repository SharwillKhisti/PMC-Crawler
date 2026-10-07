import json

# Load the dataset inventory we already created
with open("pmc_datasets.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Handle either a direct list or an API-style response
if isinstance(data, list):
    datasets = data
elif isinstance(data, dict):
    datasets = (
        data.get("content")
        or data.get("data")
        or data.get("datasets")
        or []
    )
else:
    datasets = []

print("\n" + "=" * 80)
print("PMC DATASETS")
print("=" * 80)

for i, dataset in enumerate(datasets, start=1):
    name = (
        dataset.get("datasetTitle")
        or dataset.get("title")
        or dataset.get("name")
        or "Unnamed Dataset"
    )

    print(f"{i:3}. {name}")

print("=" * 80)
print(f"Total datasets: {len(datasets)}")
print("=" * 80)