import requests
import pymupdf
import csv
import os
import re

URL = "https://opendata.pmc.gov.in/opendata/PMCReports/PMC-Water-Supply-Brochure.pdf"

OUTPUT_DIR = "pmc_water"
PDF_FILE = os.path.join(OUTPUT_DIR, "water_report.pdf")
TEXT_FILE = os.path.join(OUTPUT_DIR, "water_text.txt")
CSV_FILE = os.path.join(OUTPUT_DIR, "water_dataset.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Downloading PMC water report...")

response = requests.get(URL, timeout=60)
response.raise_for_status()

with open(PDF_FILE, "wb") as f:
    f.write(response.content)

print("Downloaded.")

# -------------------------
# Extract PDF text
# -------------------------

doc = pymupdf.open(PDF_FILE)

all_text = ""

for page_num, page in enumerate(doc):
    text = page.get_text("text")

    all_text += f"\n--- PAGE {page_num + 1} ---\n"
    all_text += text

doc.close()

with open(TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(all_text)

print("Text extracted.")

# -------------------------
# Helper functions
# -------------------------

def find_number(patterns, text):
    """
    Try multiple regex patterns and return the first match.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            value = match.group(1)
            value = value.replace(",", "").strip()

            try:
                return float(value)
            except ValueError:
                return value

    return None


records = []

# -------------------------
# WATER SUPPLY METRICS
# -------------------------

existing_plants = find_number([
    r"existing.*?(\d+)\s*treatment\s*plants",
    r"(\d+)\s*treatment\s*plants",
], all_text)

existing_capacity = find_number([
    r"existing.*?treatment.*?capacity.*?([\d,]+)\s*MLD",
    r"([\d,]+)\s*MLD.*?existing",
    r"treatment capacity.*?([\d,]+)\s*MLD",
], all_text)

planned_capacity = find_number([
    r"additional.*?capacity.*?([\d,]+)\s*MLD",
    r"planned.*?capacity.*?([\d,]+)\s*MLD",
    r"under.*?construction.*?([\d,]+)\s*MLD",
], all_text)

population_2047 = find_number([
    r"served population.*?2047.*?([\d,]+)",
    r"population.*?2047.*?([\d,]+)",
], all_text)

demand_2047 = find_number([
    r"demand.*?2047.*?([\d,]+)\s*MLD",
    r"2047.*?demand.*?([\d,]+)\s*MLD",
], all_text)

existing_reservoirs = find_number([
    r"existing.*?(?:SRs|reservoirs).*?(\d+)",
    r"(\d+).*?existing.*?(?:SRs|reservoirs)",
], all_text)

existing_storage = find_number([
    r"existing storage capacity.*?([\d,]+)\s*ML",
    r"storage capacity.*?([\d,]+)\s*ML",
], all_text)

proposed_reservoirs = find_number([
    r"proposed.*?(?:new )?(?:SRs|reservoirs).*?(\d+)",
    r"(\d+).*?proposed.*?(?:SRs|reservoirs)",
], all_text)

additional_storage = find_number([
    r"additional storage capacity.*?([\d,]+)\s*ML",
], all_text)


# -------------------------
# Add records
# -------------------------

metrics = [
    ("Existing treatment plants", existing_plants, "plants"),
    ("Existing treatment capacity", existing_capacity, "MLD"),
    ("Planned/under-construction treatment capacity", planned_capacity, "MLD"),
    ("Population served in 2047", population_2047, "people"),
    ("Water demand in 2047", demand_2047, "MLD"),
    ("Existing service reservoirs", existing_reservoirs, "count"),
    ("Existing storage capacity", existing_storage, "ML"),
    ("Proposed service reservoirs", proposed_reservoirs, "count"),
    ("Additional storage capacity", additional_storage, "ML"),
]

for indicator, value, unit in metrics:

    if value is not None:
        records.append({
            "domain": "water",
            "indicator": indicator,
            "value": value,
            "unit": unit,
            "source": URL
        })

# -------------------------
# Save CSV
# -------------------------

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "domain",
            "indicator",
            "value",
            "unit",
            "source"
        ]
    )

    writer.writeheader()
    writer.writerows(records)

print()
print("Created:", CSV_FILE)
print("Relevant records:", len(records))

for record in records:
    print(
        f"{record['indicator']}: "
        f"{record['value']} {record['unit']}"
    )