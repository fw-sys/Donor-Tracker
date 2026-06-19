cat > ~/Documents/update_foerderung.py << 'EOF'
#!/usr/bin/env python3
import os, json, sys, traceback, re, anthropic
from datetime import datetime

PROMPT = """Suche nach aktuellen Förderprogrammen für eine Hamburger Buchhandlungs-GmbH
die 2 neue Filialen eröffnet. Antworte abschließend mit einem JSON-Array.
Jedes Programm: id, name, traeger, art (Zuschuss oder Kredit), ebene (Bund/Land/Kommune),
betrag, deadline (YYYY-MM-DD oder null), zweck, antragsweg, beschreibung, url.
8-12 Programme. art = exakt 'Zuschuss' oder 'Kredit'. ebene = exakt 'Bund', 'Land' oder 'Kommune'."""

def clean_json(text):
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    return text.strip()

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("FEHLER: Key fehlt")
        sys.exit(1)
    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("Starte Recherche...")
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=16000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": PROMPT}],
        )
        print(f"Stop reason: {response.stop_reason}")

        # Alle Text-Blöcke zusammenführen
        all_text = " ".join(b.text for b in response.content if hasattr(b, 'text') and b.text)

        # JSON-Array aus dem Text extrahieren
        match = re.search(r'\[\s*\{.*\}\s*\]', all_text, re.DOTALL)
        if not match:
            print("FEHLER: Kein JSON-Array gefunden")
            print(f"Text: {all_text[:500]}")
            sys.exit(1)

        programs = json.loads(match.group())
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
EOF

python3 ~/Documents/update_foerderung.py
