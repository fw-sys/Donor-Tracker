#!/usr/bin/env python3
import os, sys, traceback

try:
    import anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    with open("debug.log", "w") as f:
        f.write(f"Key vorhanden: {'ja' if api_key else 'NEIN'}\n")
        f.write(f"Key Länge: {len(api_key)}\n")
        f.write(f"Key Anfang: {api_key[:12]}...\n")
        
        client = anthropic.Anthropic(api_key=api_key)
        f.write("Client erstellt\n")
        
        r = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=50,
            messages=[{"role": "user", "content": "Sag nur: OK"}],
        )
        f.write(f"Antwort: {r.content[0].text}\n")
        f.write("ERFOLG\n")

except Exception as e:
    with open("debug.log", "a") as f:
        f.write(f"FEHLER: {type(e).__name__}: {e}\n")
        f.write(traceback.format_exc())
    sys.exit(1)
