import requests

def find_leaked_domains(email):
    print("🔓 Suche Leaks (HaveIBeenPwned)…")
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": "DEIN_API_KEY",
        "user-agent": "TraceGlobe"
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return [b['Domain'] for b in res.json()]
    except:
        pass
    return []
