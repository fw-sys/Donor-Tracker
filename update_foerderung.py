#!/usr/bin/env python3
import os, json, sys, anthropic
from datetime import datetime

def main():
    # Prüfen ob API-Key vorhanden
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("FEHLER: ANTHROPIC_API_KEY ist nicht gesetzt!")
        sys.exit(1)
    print(f"API-Key gefunden: {api_key[:8]}...")

    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("Client erstellt, sende Anfrage...")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": "Antworte nur mit: [{}]"}],
        )
        print("Antwort erhalten!")
        print(f"Stop-Reason: {response.stop_reason}")
        for block in response.content:
            print(f"Block-Typ: {block.type}")

    except Exception as e:
        print(f"FEHLER: {type(e).__name__}: {e}")
        sys.exit(1)

    print("Test erfolgreich.")

if __name__ == "__main__":
    main()
