import requests
import re
from dotenv import load_dotenv

load_dotenv()  # lädt .env-Datei aus dem Projektverzeichnis

API_KEY = os.getenv("SERPER_API_KEY")

def find_dork_domains(email):
    print("🕵️ Starte echte Google-Dorking-Suche über serper.dev...")
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": f'"{email}"',
        "gl": "us",
        "hl": "en"
    }

    try:
        res = requests.post("https://google.serper.dev/search", json=data, headers=headers)
        res.raise_for_status()
        json_data = res.json()
        urls = [r["link"] for r in json_data.get("organic", [])]
        domains = set(re.findall(r"https?://([\w.-]+)/?", " ".join(urls)))
        print(f"✅ {len(domains)} Domains gefunden über serper.dev")
        return domains
    except Exception as e:
        print(f"❌ Fehler bei serper.dev-Abfrage: {e}")
        return set()
