import urllib.request

try:
    with urllib.request.urlopen("http://localhost:8000/docs") as response:
        print(f"Server is up. Status: {response.getcode()}")
except Exception as e:
    print(f"Server check failed: {e}")
