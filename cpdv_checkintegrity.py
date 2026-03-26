#!/usr/bin/env python3

# This checkintegrity.py checks for empty chapters in the CPDV JSON files.

import json
from pathlib import Path

base = Path("cpdv-json")
skip = "EntireBible-NABRE.json"

results = []
for p in sorted(base.glob("*.json")):
    if p.name == skip:
        continue
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    empty = []
    for ch_key, ch_val in data.items():
        if isinstance(ch_val, dict) and len(ch_val) == 0:
            empty.append(ch_key)
    if empty:
        results.append((p.name, sorted(empty, key=lambda x: int(x) if str(x).isdigit() else x)))

for name, chapters in results:
    print(f"{name}: empty chapters {chapters}")

if not results:
    print("No books with empty chapter objects found.")
else:
    print(f"\nTotal: {len(results)} book(s)")