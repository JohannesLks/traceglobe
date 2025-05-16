import requests
from bs4 import BeautifulSoup

def fetch_privacy_policy(domain):
    print(f"📄 Suche Datenschutzerklärung auf {domain}...")
    for path in ["/privacy", "/privacy-policy", "/legal", "/terms"]:
        try:
            url = f"https://{domain}{path}"
            res = requests.get(url, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                return soup.get_text(separator=" ", strip=True)
        except:
            continue
    return ""
