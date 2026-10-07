import requests

BASE = "https://opendataapi.pmc.gov.in/"

file_ids = [1182, 1181, 1180]

endpoints = [
    "dataset-files/{id}",
    "dataset-files/{id}/download",
    "dataset-files/{id}/file",
    "dataset-files/{id}/download-file",
    "dataset-files/{id}/downloadFile",
]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
}

for file_id in file_ids:
    print("\n" + "=" * 100)
    print("FILE ID:", file_id)
    print("=" * 100)

    for pattern in endpoints:
        endpoint = pattern.format(id=file_id)
        url = BASE + endpoint

        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=20,
                allow_redirects=False
            )

            print("\n", endpoint)
            print("Status:", r.status_code)
            print("Content-Type:", r.headers.get("Content-Type"))
            print("Location:", r.headers.get("Location"))
            print("Length:", len(r.content))

            if "application/json" in (r.headers.get("Content-Type") or ""):
                print(r.text[:1000])
            else:
                print("First bytes:", r.content[:100])

        except Exception as e:
            print("ERROR:", e)