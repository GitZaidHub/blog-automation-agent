import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    with urllib.request.urlopen(URL) as response:
        data = json.loads(response.read().decode('utf-8'))
        models = data.get("models", [])
        print("Available Models:")
        for m in models:
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print(f"- {m['name']}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Exception: {e}")
