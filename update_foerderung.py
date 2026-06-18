#!/usr/bin/env python3
import os, json, anthropic
from datetime import datetime

PROMPT = """Du bist ein deutscher Fördermittelexperte. Recherchiere aktuell verfügbare
Förderprogramme für folgendes Unternehmen:

Unternehmen: Buchhandlung Wassermann GmbH, Hamburg
Vorhaben: Eröffnung von 2 neuen Filialen in Hamburg im Oktober 2026
Förderarten: Zuschüsse und Darlehen/Kredite
Branche: Einzelhandel / Buchhandel

Durchsuche: IFB Hamburg, KfW, BAFA, Hamburg Invest, Handelskammer Hamburg,
Kulturbehörde Hamburg, ESF Plus, BMWK go-digital.

Antworte NUR mit einem JSON-Array, kein Text drumherum, keine Backticks:
[
  {
    "id": "eindeutige-id",
    "name": "Programmname",
    "traeger": "Förderträger",
    "art": "Zuschuss",
    "ebene": "Land",
    "betrag": "bis 50.000 €",
    "deadline": "YYYY-MM-DD oder null",
    "zweck": "z.B. Investition, Betriebsmittel",
    "antragsweg": "z.B. über Hausbank",
    "beschreibung": "2-3 Sätze warum passend",
    "url": "https://..."
  }
]
8-12 reale, aktuell aktive Programme. art = 'Zuschuss' oder 'Kredit'. ebene = 'Bund', 'Land' oder 'Kommune'."""

def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": PROMPT}],
    )
    result_text = next((b.text for b in response.content if b.type == "text"), "")
    clean = result_text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    programs = json.loads(clean)
    output = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at_de": datetime.now().strftime("%d.%m.%Y %H:%M Uhr"),
        "programs": programs,
    }
    with open("foerderung.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Fertig: {len(programs)} Programme gespeichert.")

if __name__ == "__main__":
    main()
