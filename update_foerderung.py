#!/usr/bin/env python3
import os, json, sys, traceback, anthropic
from datetime import datetime

PROMPT = """Du bist ein deutscher Fördermittelexperte. Recherchiere die aktuell verfügbaren
Förderprogramme für folgendes Unternehmen:

Unternehmen: Buchhandlung Wassermann GmbH, Hamburg (GmbH, gegründet 1848)
Vorhaben: Eröffnung von 2 neuen Filialen in Hamburg im Oktober 2026
Gewünschte Förderarten: Zuschüsse (nicht rückzahlbar) und Darlehen/Kredite
Standorte: beide neuen Filialen in Hamburg
Branche: Einzelhandel / Buchhandel / Kultur

Durchsuche aktuelle Quellen: IFB Hamburg, KfW, BAFA, Hamburg Invest,
Handelskammer Hamburg, Kulturbehörde Hamburg, ESF Plus, BMWK go-digital.

Antworte NUR mit einem JSON-Array. Kein Text davor oder danach, keine Backticks:
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
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("FEHLER: ANTHROPIC_API_KEY nicht gesetzt")
        sys.exit(1)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("Starte Recherche...")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": PROMPT}],
        )

        result_text = next((b.text for b in response.content if b.type == "text"), "")
        clean = result_text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        programs = json.loads(clean)
        print(f"{len(programs)} Programme gefunden.")

        output = {
            "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated_at_de": datetime.now().strftime("%d.%m.%Y %H:%M Uhr"),
            "programs": programs,
        }

        with open("foerderung.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("foerderung.json gespeichert.")

    except Exception as e:
        print(f"FEHLER: {type(e).__name__}: {e}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
