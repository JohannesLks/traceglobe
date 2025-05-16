import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")

def extract_identifier(email):
    return email.split("@")[0]

def find_dork_domains(email):
    domains = set()
    identifier = extract_identifier(email)
    queries = [
        f'"{email}"',                    # exakte Mailadresse
        f'"{identifier}"',              # nur Benutzername
        f'{identifier} site:github.com',# GitHub-Erwähnungen
        f'{identifier} site:pastebin.com',
        f'{identifier} filetype:txt',
    ]

    # Google Dorking via serper.dev
    if API_KEY:
        for q in queries:
            print(f"🕵️ Suche mit serper.dev: {q}")
            headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
            data = {"q": q, "gl": "us", "hl": "en"}
            try:
                res = requests.post("https://google.serper.dev/search", json=data, headers=headers)
                res.raise_for_status()
                json_data = res.json()
                urls = [r["link"] for r in json_data.get("organic", [])]
                found = set(re.findall(r"https?://([\w.-]+)", " ".join(urls)))
                print(f"✅ {len(found)} Domains aus '{q}' gefunden")
                domains.update(found)
            except Exception as e:
                print(f"❌ Fehler bei serper.dev-Abfrage: {e}")
    else:
        print("⚠️ Kein SERPER_API_KEY gesetzt – überspringe Google-Dorking.")

    # Fallback DuckDuckGo Scraping
    if not domains:
        print("🕸️ Fallback: DuckDuckGo Scraping aktiv…")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            for q in queries:
                print(f"🕸️ Suche mit DuckDuckGo: {q}")
                url = f"https://html.duckduckgo.com/html?q={q}"
                res = requests.get(url, headers=headers, timeout=10)
                urls = re.findall(r'href="(https?://[^"]+)"', res.text)
                found = set(re.findall(r"https?://([\w.-]+)", " ".join(urls)))
                print(f"✅ {len(found)} Domains aus '{q}' gefunden")
                domains.update(found)
        except Exception as e:
            print(f"❌ DuckDuckGo-Fehler: {e}")

    return domains
