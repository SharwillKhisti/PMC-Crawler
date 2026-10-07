import pandas as pd
import re

df = pd.read_csv("pmc_inventory.csv")

print("=" * 80)
print("PMC DATA INVENTORY PROFILE")
print("=" * 80)

print()
print("Dataset records:", df["datasetId"].nunique())
print("File records:", len(df))


# --------------------------------------------------
# 1. FILE FORMAT DISTRIBUTION
# --------------------------------------------------

print()
print("=" * 80)
print("FILE FORMATS")
print("=" * 80)

formats = (
    df["format"]
    .fillna("UNKNOWN")
    .str.upper()
    .value_counts()
)

print(formats.to_string())


# --------------------------------------------------
# 2. DATASETS WITH MULTIPLE FILES
# --------------------------------------------------

print()
print("=" * 80)
print("DATASETS WITH MULTIPLE FILES")
print("=" * 80)

file_counts = (
    df.groupby(["datasetId", "datasetTitle"])
    .size()
    .sort_values(ascending=False)
)

print(
    file_counts[file_counts > 1]
    .head(30)
    .to_string()
)


# --------------------------------------------------
# 3. SEARCH FOR ANALYTICALLY INTERESTING DATASETS
# --------------------------------------------------

keywords = [
    "ward",
    "daily",
    "monthly",
    "year",
    "yearly",
    "annual",
    "tax",
    "water",
    "waste",
    "sewage",
    "traffic",
    "road",
    "school",
    "hospital",
    "energy",
    "electric",
    "pollution",
    "air",
    "environment",
    "property",
    "collection",
    "consumption",
    "population",
    "birth",
    "death",
    "complaint",
    "grievance",
    "vehicle",
    "transport",
    "rainfall",
    "rain",
    "temperature",
    "health",
    "disease",
    "building",
    "license",
]

pattern = "|".join(map(re.escape, keywords))

text = (
    df["datasetTitle"].fillna("")
    + " "
    + df["metaData"].fillna("")
    + " "
    + df["tags"].fillna("")
).str.lower()

interesting = df[text.str.contains(pattern, regex=True, na=False)]

interesting = interesting[
    [
        "datasetId",
        "datasetTitle",
        "format",
        "fileSize",
        "createdDate",
        "modifiedDate",
        "metaData",
        "tags",
    ]
].drop_duplicates("datasetId")


print()
print("=" * 80)
print("POTENTIALLY ANALYTICAL DATASETS")
print("=" * 80)

print("Found:", len(interesting))

for _, row in interesting.iterrows():

    print()
    print(f"[{row['datasetId']}] {row['datasetTitle']}")
    print(f"    Format: {row['format']}")
    print(f"    Size: {row['fileSize']}")
    print(f"    Metadata: {row['metaData']}")


# --------------------------------------------------
# 4. MACHINE-READABLE FILES
# --------------------------------------------------

machine_formats = [
    ".CSV",
    ".XLS",
    ".XLSX",
    ".JSON",
    ".GEOJSON",
    ".XML",
    ".ZIP",
]

machine = df[
    df["format"]
    .fillna("")
    .str.upper()
    .isin(machine_formats)
]

print()
print("=" * 80)
print("MACHINE-READABLE FILES")
print("=" * 80)

print("Files:", len(machine))
print("Datasets:", machine["datasetId"].nunique())

print()

print(
    machine[
        [
            "datasetId",
            "datasetTitle",
            "format",
            "fileSize",
            "metaData",
        ]
    ]
    .drop_duplicates()
    .to_string(index=False)
)


# --------------------------------------------------
# 5. SAVE ANALYTICAL SHORTLIST
# --------------------------------------------------

interesting.to_csv(
    "pmc_analytical_candidates.csv",
    index=False,
    encoding="utf-8-sig"
)

machine.to_csv(
    "pmc_machine_readable.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("Saved:")
print("  pmc_analytical_candidates.csv")
print("  pmc_machine_readable.csv")