import urllib.request
import json

try:
    with urllib.request.urlopen("http://localhost:8000/status/nonexistent-id-12345") as response:
        print(f"Status Code: {response.getcode()}")
        print(f"Response Body: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
except Exception as e:
    print(f"Error: {e}")
