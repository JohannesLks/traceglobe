import spacy
import re

nlp = spacy.load("en_core_web_sm")
BLACKLIST = {"privacy policy", "data", "cookies", "terms", "personal information"}

def extract_companies(text):
    doc = nlp(text)
    orgs = set()
    for ent in doc.ents:
        if ent.label_ == "ORG":
            name = ent.text.strip()
            name_lower = name.lower()
            if len(name) > 2 and not re.search(r"[^\w\s\-.]", name) and name_lower not in BLACKLIST:
                orgs.add(name)
    return orgs
