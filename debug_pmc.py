import requests

url = "https://opendataapi.pmc.gov.in/dataset-files"

r = requests.get(url, timeout=30)

print("=" * 60)
print("STATUS:", r.status_code)
print("URL:", r.url)
print("CONTENT-TYPE:", r.headers.get("content-type"))
print("=" * 60)

print(r.text[:20000])