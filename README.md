# Catholic Public Domain Bible (CPDV) in JSON

This cpdv.py project, written in Python, converts the Catholic Public Domain Bible (CPDV) into JSON format. 

Originally, it was a direct Python translation of the Groovy script CPDVJSONEncoder.groovy by **Steve Bruno's [CPDV-JSON](https://bitbucket.org/sbruno/cpdv-json-encoder/)** project, but has now since been largely modified to be more Python native.

Catholic Public Domain Version of the Bible is edited and translated by **Ronald L. Conte Jr** and can be found at: https://www.sacredbible.org/index.htm


## Overview

The Python script `cpdv.py` downloads the HTML files from the Sacred Bible website and converts them into JSON format. The JSON files are saved in the CPDV-JSON directory with both Old Testament (OT) and New Testament (NT) books. 

The script also creates a combined JSON file called EntireBible-CPDV.json.

## Usage

```bash
python3 cpdv.py
```

## Updates

- **16 Mar 2026**: Fixes so that now Book of Revelations now were able to be parsed into Json. Reparsed all books in cpdv-json folder with fixes.
- **10 Nov 2025**: Initial release includes all the latest errata corrections up 26 February 2025. Errata corrections are available at: https://www.sacredbible.org/errata.htm
