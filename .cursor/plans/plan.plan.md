# Translate Groovy Script to Python

## Overview

Translate `CPDVJSONEncoder.groovy` to Python in `cpdv.py`, maintaining equivalent functionality for downloading, parsing, and converting Bible text to JSON.

## Implementation Details

### Functions to Translate:

1. **`download(address)`** → `download(address)`

- Use `urllib.request` to download files
- Save to local file with same naming convention

2. **`toJson(bookName, bibleMap)`** → `to_json(book_name, bible_map)`

- Download HTML file using `download()`
- Read file with `windows-1252` encoding (Python `encoding='windows-1252'`)
- Parse lines starting with `{`
- Extract chapter and verse from metadata (format: `{chapter:verse}`)
- Remove `<BR>` tags
- Convert content to UTF-8 using proper encoding handling
- Build nested dictionary: `book[chapter][verse] = content`
- Write individual JSON files to `CPDV-JSON/` directory
- Optionally update `bible_map` dictionary
- Delete temporary HTML file

3. **`toUrl(bookName)`** → `to_url(book_name)`

- Simple string concatenation for URL construction

4. **Main execution**

- Create `CPDV-JSON` directory if it doesn't exist (`os.makedirs`)
- Call `to_json()` for all 66 books (45 OT + 27 NT)
- Track execution time
- Write combined `EntireBible-CPDV.json` file

### Python Libraries Needed:

- `urllib.request` for downloading
- `json` for JSON encoding
- `os` for directory operations
- `time` for timing execution

### Key Translation Notes:

- Groovy maps (`[:]`) → Python dictionaries (`{}`)
- Groovy `JsonBuilder` → Python `json.dumps()` with `indent` parameter
- Groovy string methods → Python string methods
- Groovy `getText("windows-1252")` → Python `open(file, encoding='windows-1252').read()`
- Groovy `each` → Python `for` loops
- File operations: Groovy `File` → Python `open()` and `os.remove()`