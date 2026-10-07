import requests
import json

url = "https://opendataapi.pmc.gov.in/dataset-files"

params = {
    "page": 0,
    "size": 10
}

r = requests.get(url, params=params, timeout=30)

print("URL:", r.url)
print("STATUS:", r.status_code)
print()

data = r.json()

print(json.dumps(data, indent=2)[:10000])