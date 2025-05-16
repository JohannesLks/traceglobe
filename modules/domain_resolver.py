import requests
from dotenv import load_dotenv

load_dotenv()  # lädt .env-Datei aus dem Projektverzeichnis

API_KEY = os.getenv("CLEARBIT_API_KEY")

def org_to_domain(company_name):
    print(f"🌐 Suche Domain für: {company_name}")
    try:
        url = f"https://company.clearbit.com/v2/companies/find?name={company_name}"
        headers = {"Authorization": f"Bearer {CLEARBIT_KEY}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json().get("domain")
    except:
        pass
    return None
