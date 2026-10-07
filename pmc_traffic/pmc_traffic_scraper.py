import requests
import pymupdf
import os
import json
import csv

PDF_URL = "https://opendata.pmc.gov.in/opendata/PMCReports/PSCDCL-Smart-City-Proposal-Presentation.pdf"

OUTPUT_DIR = "pmc_traffic"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(IMAGE_DIR, exist_ok=True)

print("Downloading PMC traffic report...")

response = requests.get(PDF_URL, timeout=30)
response.raise_for_status()

pdf_path = os.path.join(OUTPUT_DIR, "report.pdf")

with open(pdf_path, "wb") as f:
    f.write(response.content)

print("Report downloaded.")

doc = pymupdf.open(pdf_path)

dataset = []

for page_number, page in enumerate(doc, start=1):

    page_text = page.get_text("text").strip()

    # Only process pages related to traffic
    traffic_keywords = [
        "traffic",
        "signal",
        "parking",
        "CCTV",
        "congestion",
        "road",
        "transport"
    ]

    is_relevant = any(
        keyword.lower() in page_text.lower()
        for keyword in traffic_keywords
    )

    if not is_relevant:
        continue

    for image_number, image in enumerate(
        page.get_images(full=True), start=1
    ):

        xref = image[0]

        image_data = doc.extract_image(xref)

        width = image_data["width"]
        height = image_data["height"]
        extension = image_data["ext"]

        # Ignore tiny logos/icons
        if width < 200 or height < 200:
            continue

        filename = (
            f"page_{page_number}_image_{image_number}.{extension}"
        )

        filepath = os.path.join(IMAGE_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(image_data["image"])

        file_size = os.path.getsize(filepath)

        dataset.append({
            "page": page_number,
            "filename": filename,
            "width": width,
            "height": height,
            "format": extension,
            "file_size_bytes": file_size,
            "source": PDF_URL,
            "page_text": page_text[:1000]
        })

print(f"Traffic-related images extracted: {len(dataset)}")

# JSON
json_path = os.path.join(OUTPUT_DIR, "dataset.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

# CSV
csv_path = os.path.join(OUTPUT_DIR, "dataset.csv")

fields = [
    "page",
    "filename",
    "width",
    "height",
    "format",
    "file_size_bytes",
    "source",
    "page_text"
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(f, fieldnames=fields)

    writer.writeheader()
    writer.writerows(dataset)

print("Created:")
print("  dataset.json")
print("  dataset.csv")
print("  images/")