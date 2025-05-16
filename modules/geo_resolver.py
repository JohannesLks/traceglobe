import socket
import requests
from ipwhois import IPWhois
import folium

def is_valid_hostname(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except:
        return False

def resolve_company_location(company):
    if not is_valid_hostname(company):
        print(f"⚠️ Ungültiger Hostname: {company}")
        return None

    try:
        ip = socket.gethostbyname(company)
        geo = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
        loc = geo.get("loc", "0,0").split(",")

        whois_data = IPWhois(ip).lookup_rdap(depth=1)
        return {
            "company": company,
            "ip": ip,
            "city": geo.get("city"),
            "region": geo.get("region"),
            "country": geo.get("country"),
            "asn": whois_data.get("asn"),
            "asn_description": whois_data.get("asn_description"),
            "asn_country": whois_data.get("asn_country_code"),
            "lat": float(loc[0]),
            "lon": float(loc[1])
        }
    except Exception as e:
        print(f"❌ WHOIS/Geo Fehler bei {company}: {e}")
        return None

def visualize_locations(locations, output_file="traceglobe_map.html"):
    print("🗺️ Erzeuge interaktive Karte…")
    m = folium.Map(location=[20, 0], zoom_start=2)

    for loc in locations:
        tooltip = f"{loc['company']}<br>IP: {loc['ip']}<br>ASN: {loc['asn']}<br>Ort: {loc['city']}, {loc['country']}"
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=folium.Popup(tooltip, max_width=300),
            tooltip=loc["company"]
        ).add_to(m)

    m.save(output_file)
    print(f"✅ Karte gespeichert unter: {output_file}")
