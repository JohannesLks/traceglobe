from modules.leaks import find_leaked_domains
from modules.dorks import find_dork_domains
from modules.crawler import fetch_privacy_policy
from modules.nlp_extract import extract_companies
from modules.geo_resolver import resolve_company_location, visualize_locations
from modules.domain_resolver import org_to_domain

def trace_email(email):
    print(f"\n🔍 Starte TraceGlobe Analyse für: {email}\n")

    domains = set()
    domains.update(find_leaked_domains(email))
    domains.update(find_dork_domains(email))

    print(f"🌐 Gefundene Domains: {domains}\n")

    companies = set()
    for domain in domains:
        text = fetch_privacy_policy(domain)
        if text:
            companies.update(extract_companies(text))

    print(f"\n🏢 Gefundene Firmen mit potenzieller Datenweitergabe ({len(companies)}):")
    for c in sorted(companies):
        print("  -", c)

    locations = []
    print("\n🌍 Versuche Domains zu den Firmen zu finden und sie zu lokalisieren…")
    for company in companies:
        domain = org_to_domain(company)
        if domain:
            loc = resolve_company_location(domain)
            if loc:
                loc["company"] = company
                locations.append(loc)

    if not locations:
        print("\n⚠️ Keine gültigen Serverstandorte gefunden.")
    else:
        print("\n📍 Lokalisierte Firmenserver:")
        for loc in locations:
            print(f"{loc['company']} – {loc['ip']} – {loc['city']}, {loc['country']} – ASN: {loc['asn']}")
        visualize_locations(locations)

if __name__ == "__main__":
    target = input("Gib die E-Mail-Adresse ein: ")
    trace_email(target.strip())
