import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import csv
import time
import os

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

START_URLS = [
    "https://opendata.pmc.gov.in/",
    "https://opendata.pmc.gov.in/datasets",
    "https://opendata.pmc.gov.in/pmc-reports",
]

ALLOWED_DOMAINS = {
    "opendata.pmc.gov.in"
}

MAX_PAGES = 500
DELAY = 0.5

OUTPUT_FILE = "pmc_sources.csv"

HEADERS = {
    "User-Agent": "PMC-Data-Research-Crawler/1.0"
}

# --------------------------------------------------
# FILE TYPE DETECTION
# --------------------------------------------------

def detect_type(url):

    lower = url.lower().split("?")[0]

    if lower.endswith(".csv"):
        return "CSV"

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return "Excel"

    if lower.endswith(".json"):
        return "JSON"

    if lower.endswith(".xml"):
        return "XML"

    if lower.endswith(".geojson"):
        return "GeoJSON"

    if lower.endswith(".zip"):
        return "ZIP"

    if lower.endswith(".pdf"):
        return "PDF"

    return "Webpage"


# --------------------------------------------------
# DOMAIN CHECK
# --------------------------------------------------

def is_allowed(url):

    parsed = urlparse(url)

    return parsed.netloc in ALLOWED_DOMAINS


# --------------------------------------------------
# NORMALIZE URL
# --------------------------------------------------

def normalize_url(url):

    parsed = urlparse(url)

    # Remove fragments
    parsed = parsed._replace(fragment="")

    return parsed.geturl()


# --------------------------------------------------
# CRAWLER
# --------------------------------------------------

queue = deque()

for url in START_URLS:
    queue.append(url)

visited = set()
results = []

session = requests.Session()
session.headers.update(HEADERS)

print("Starting PMC crawler...")
print()

while queue and len(visited) < MAX_PAGES:

    url = queue.popleft()

    url = normalize_url(url)

    if url in visited:
        continue

    if not is_allowed(url):
        continue

    visited.add(url)

    print(f"[{len(visited)}/{MAX_PAGES}] {url}")

    try:

        response = session.get(
            url,
            timeout=15
        )

        status = response.status_code

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        resource_type = detect_type(url)

        results.append({
            "url": url,
            "type": resource_type,
            "status": status,
            "content_type": content_type,
            "source_page": ""
        })

        if status != 200:
            continue

        # --------------------------------------------------
        # Don't parse binary files
        # --------------------------------------------------

        if resource_type != "Webpage":
            continue

        # --------------------------------------------------
        # Parse HTML
        # --------------------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = ""

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        # Update last result with title
        results[-1]["title"] = title

        # --------------------------------------------------
        # Extract links
        # --------------------------------------------------

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link["href"].strip()

            if not href:
                continue

            next_url = urljoin(
                url,
                href
            )

            next_url = normalize_url(
                next_url
            )

            if not is_allowed(next_url):
                continue

            if next_url not in visited:

                queue.append(next_url)

        time.sleep(DELAY)

    except requests.RequestException as e:

        print(
            "  ERROR:",
            str(e)
        )

        results.append({
            "url": url,
            "type": "ERROR",
            "status": "",
            "content_type": "",
            "source_page": "",
            "title": ""
        })


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

fieldnames = [
    "url",
    "type",
    "status",
    "content_type",
    "title",
    "source_page"
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for row in results:

        for field in fieldnames:

            if field not in row:
                row[field] = ""

        writer.writerow(row)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print()
print("=" * 50)
print("CRAWL COMPLETE")
print("=" * 50)

print("Pages visited:", len(visited))
print("Resources found:", len(results))
print()

counts = {}

for row in results:

    resource_type = row["type"]

    counts[resource_type] = (
        counts.get(resource_type, 0) + 1
    )

for resource_type, count in sorted(
    counts.items()
):

    print(
        f"{resource_type:12} : {count}"
    )

print()
print(
    "Saved:",
    os.path.abspath(OUTPUT_FILE)
)