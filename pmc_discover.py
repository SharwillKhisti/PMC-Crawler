import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://opendata.pmc.gov.in/datasets"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers,
    timeout=20
)

print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("HTML length:", len(response.text))

print("\n" + "=" * 60)
print("LINKS")
print("=" * 60)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

for a in soup.find_all("a", href=True):

    href = a["href"].strip()
    text = a.get_text(" ", strip=True)

    print(
        f"{text[:60]:60} -> {href}"
    )


print("\n" + "=" * 60)
print("SCRIPTS")
print("=" * 60)

for script in soup.find_all("script"):

    src = script.get("src")

    if src:
        print(
            "SCRIPT:",
            urljoin(URL, src)
        )

    else:

        content = script.get_text()

        if content.strip():

            print(
                "\nINLINE SCRIPT:\n",
                content[:2000]
            )


print("\n" + "=" * 60)
print("POSSIBLE API / DATA REFERENCES")
print("=" * 60)

keywords = [
    "api",
    "json",
    "ajax",
    "fetch",
    "dataset",
    "download",
    "csv",
    "xlsx",
    "xls",
    "geojson",
    "arcgis",
    "FeatureServer",
    "MapServer"
]

html_lower = response.text.lower()

for keyword in keywords:

    if keyword.lower() in html_lower:

        print(
            "FOUND:",
            keyword
        )