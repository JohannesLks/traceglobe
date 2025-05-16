import requests
import re

def org_to_domain(company_name):
    print(f"🌐 Suche Domain für Firma via DuckDuckGo: {company_name}")
    try:
        q = f"{company_name} official website"
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://html.duckduckgo.com/html?q={q}"
        res = requests.get(url, headers=headers, timeout=10)
        matches = re.findall(r'https?://([a-zA-Z0-9.-]+\.[a-z]{2,})', res.text)
        domains = [d for d in matches if not d.startswith("duckduckgo")]
        if domains:
            print(f"✅ Beste Domain gefunden: {domains[0]}")
            return domains[0]
    except Exception as e:
        print(f"❌ DuckDuckGo-Fehler: {e}")
    return None
