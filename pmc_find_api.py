import requests
import re

BASE = "https://opendata.pmc.gov.in"

JS_URL = (
    BASE +
    "/_next/static/chunks/app/datasets/"
    "page-eaf68fd7a493cd4f.js"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Downloading dataset JavaScript...")
print(JS_URL)
print()

response = requests.get(
    JS_URL,
    headers=headers,
    timeout=20
)

print("Status:", response.status_code)
print("Length:", len(response.text))

js = response.text

# Save it so we can inspect it
with open(
    "datasets_page.js",
    "w",
    encoding="utf-8"
) as f:
    f.write(js)

print("Saved datasets_page.js")

print()
print("=" * 70)
print("POSSIBLE API REFERENCES")
print("=" * 70)

# Look for strings containing API-like paths
patterns = [
    r'["\']([^"\']*api[^"\']*)["\']',
    r'["\']([^"\']*dataset[^"\']*)["\']',
    r'["\']([^"\']*datasets[^"\']*)["\']',
    r'["\']([^"\']*json[^"\']*)["\']',
    r'["\']([^"\']*download[^"\']*)["\']',
]

found = set()

for pattern in patterns:

    matches = re.findall(
        pattern,
        js,
        re.IGNORECASE
    )

    for match in matches:

        if len(match) < 300:
            found.add(match)

for item in sorted(found):

    print(item)

print()
print("=" * 70)
print("FETCH / AXIOS REFERENCES")
print("=" * 70)

# Print snippets around fetch()
for match in re.finditer(
    r'fetch\s*\(',
    js,
    re.IGNORECASE
):

    start = max(
        0,
        match.start() - 300
    )

    end = min(
        len(js),
        match.end() + 700
    )

    print()
    print(js[start:end])
    print("-" * 70)

# Look for axios calls too
for match in re.finditer(
    r'axios\.',
    js,
    re.IGNORECASE
):

    start = max(
        0,
        match.start() - 300
    )

    end = min(
        len(js),
        match.end() + 700
    )

    print()
    print(js[start:end])
    print("-" * 70)