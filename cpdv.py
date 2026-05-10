#!/usr/bin/env python3

# This python script is used to convert the Catholic Public Domain Bible (CPDV) into JSON format.
# Please read the README.md file for more information.
# 
# https://github.com/yoarikso/cpdvbible
# 

import argparse
import json
import os
import re
import sys
import time
import urllib.request


def download(address):
    filename = address.split("/")[-1]
    urllib.request.urlretrieve(address, filename)

    # after downloading, rename the file to OT-24_SongOfSongs.htm
    if filename == "OT-24_Song2.htm":
        os.rename(filename, "OT-24_SongOfSongs.htm")

def to_json(book_name, bible_map):
    download(to_url(book_name))

    file_html = f"{book_name}.htm"

    with open(file_html, "r", encoding="windows-1252", newline='') as f:
        genesis = f.read()

    # Revelation (and possibly other long books) use a different format: multiple verses
    # per line with lines starting with [Book N] instead of {c:v}. Use regex to find
    # all {chapter:verse} patterns in the full content, which works for both formats.
    content_clean = genesis.replace("<BR>", "")
    verse_pattern = re.compile(r'\{(\d+):(\d+)\}\s*([^{]*)')

    # Strip HTML tags and chapter anchors that appear between verses (e.g. in Revelation)
    def clean_verse_text(text):
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        # Remove any [Book_name N] chapter anchors (e.g. [Genesis 2], [Revelation 3], [1 John 2])
        text = re.sub(r'\s*\[\s*[^\[\]]+\s+\d+\s*\]\s*', ' ', text)
        # Remove trailing "The Sacred Bible: {book name}" footer that appears in the last verse
        text = re.sub(r'\s*[\r\n]+\s*The Sacred Bible:[\s\S]*$', '', text)
        return text.strip()

    book = {}
    for match in verse_pattern.finditer(content_clean):
        chapter, verse, content = match.groups()
        content = clean_verse_text(content)
        if not content:
            continue

        # Convert content to UTF-8 (matching Groovy's encode/decode cycle)
        content_utf8 = content.encode("utf-8").decode("utf-8")

        if chapter not in book:
            book[chapter] = {}

        book[chapter][verse] = content_utf8

    if bible_map is not None:
        book_name_key = book_name[book_name.index("_")+1:]
        bible_map[book_name_key] = book.copy()

    book["charset"] = "UTF-8"

    json_str = json.dumps(book, indent=4, ensure_ascii=False)

    file_json = f"cpdv-json/{book_name}.json"
    os.makedirs(os.path.dirname(file_json), exist_ok=True)
    with open(file_json, "w", encoding="utf-8") as f:
        f.write(json_str)

    os.remove(file_html)


def to_url(book_name):
    host = "http://www.sacredbible.org/catholic/"
    
    # Song of Songs is named OT-24_Song2 in the cpdv website.
    if(book_name == "OT-24_SongOfSongs"):
        book_name = "OT-24_Song2"

    return f"{host}{book_name}.htm"

def merge_entire_bible_json():
    folder = "cpdv-json"
    output_file = "EntireBible-CPDV.json"

    book_files = []
    for filename in os.listdir(folder):
        if filename == output_file or not filename.endswith(".json"):
            continue

        match = re.match(r"^(OT|NT)-(\d+)_([^.]+)\.json$", filename)
        if not match:
            continue

        testament, order, book_name_key = match.groups()
        testament_order = 0 if testament == "OT" else 1
        book_files.append((testament_order, int(order), book_name_key, filename))

    book_files.sort(key=lambda x: (x[0], x[1]))

    entire_bible = {"charset": "UTF-8"}
    for _, _, book_name_key, filename in book_files:
        file_path = os.path.join(folder, filename)
        with open(file_path, encoding="utf-8") as f:
            book_data = json.load(f)
            # Per-book files include charset; in-memory encode omits it from each book.
            book_data.pop("charset", None)
            entire_bible[book_name_key] = book_data

    file_json = os.path.join(folder, output_file)
    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(entire_bible, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Convert the Catholic Public Domain Bible (CPDV) into JSON format."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-m",
        "--merge-bible",
        action="store_true",
        help="Merge cpdv-json books into a single EntireBible-CPDV.json and exit.",
    )
    mode.add_argument(
        "-e",
        "--encode-bible",
        action="store_true",
        help="Download and encode all books into cpdv-json (and write EntireBible-CPDV.json).",
    )
    args = parser.parse_args()

    if args.merge_bible:
        merge_entire_bible_json()
        sys.exit(0)

    if not args.encode_bible:
        parser.print_help()
        sys.exit(0)

    print("Encoding CPDV Bible into JSON format")

    bible_map = {}
    bible_map["charset"] = "UTF-8"

    os.makedirs("cpdv-json", exist_ok=True)

    start_time = time.time()

    # Old Testament
    to_json("OT-01_Genesis", bible_map)
    to_json("OT-02_Exodus", bible_map)
    to_json("OT-03_Leviticus", bible_map)
    to_json("OT-04_Numbers", bible_map)
    to_json("OT-05_Deuteronomy", bible_map)
    to_json("OT-06_Joshua", bible_map)
    to_json("OT-07_Judges", bible_map)
    to_json("OT-08_Ruth", bible_map)
    to_json("OT-09_1-Samuel", bible_map)
    to_json("OT-10_2-Samuel", bible_map)
    to_json("OT-11_1-Kings", bible_map)
    to_json("OT-12_2-Kings", bible_map)
    to_json("OT-13_1-Chronicles", bible_map)
    to_json("OT-14_2-Chronicles", bible_map)
    to_json("OT-15_Ezra", bible_map)
    to_json("OT-16_Nehemiah", bible_map)
    to_json("OT-17_Tobit", bible_map)
    to_json("OT-18_Judith", bible_map)
    to_json("OT-19_Esther", bible_map)
    to_json("OT-20_Job", bible_map)
    to_json("OT-21_Psalms", bible_map)
    to_json("OT-22_Proverbs", bible_map)
    to_json("OT-23_Ecclesiastes", bible_map)
    to_json("OT-24_SongOfSongs", bible_map)
    to_json("OT-25_Wisdom", bible_map)
    to_json("OT-26_Sirach", bible_map)
    to_json("OT-27_Isaiah", bible_map)
    to_json("OT-28_Jeremiah", bible_map)
    to_json("OT-29_Lamentations", bible_map)
    to_json("OT-30_Baruch", bible_map)
    to_json("OT-31_Ezekiel", bible_map)
    to_json("OT-32_Daniel", bible_map)
    to_json("OT-33_Hosea", bible_map)
    to_json("OT-34_Joel", bible_map)
    to_json("OT-35_Amos", bible_map)
    to_json("OT-36_Obadiah", bible_map)
    to_json("OT-37_Jonah", bible_map)
    to_json("OT-38_Micah", bible_map)
    to_json("OT-39_Nahum", bible_map)
    to_json("OT-40_Habakkuk", bible_map)
    to_json("OT-41_Zephaniah", bible_map)
    to_json("OT-42_Haggai", bible_map)
    to_json("OT-43_Zechariah", bible_map)
    to_json("OT-44_Malachi", bible_map)
    to_json("OT-45_1-Maccabees", bible_map)
    to_json("OT-46_2-Maccabees", bible_map)

    # # New Testament
    to_json("NT-01_Matthew", bible_map)
    to_json("NT-02_Mark", bible_map)
    to_json("NT-03_Luke", bible_map)
    to_json("NT-04_John", bible_map)
    to_json("NT-05_Acts", bible_map)
    to_json("NT-06_Romans", bible_map)
    to_json("NT-07_1-Corinthians", bible_map)
    to_json("NT-08_2-Corinthians", bible_map)
    to_json("NT-09_Galatians", bible_map)
    to_json("NT-10_Ephesians", bible_map)
    to_json("NT-11_Philippians", bible_map)
    to_json("NT-12_Colossians", bible_map)
    to_json("NT-13_1-Thessalonians", bible_map)
    to_json("NT-14_2-Thessalonians", bible_map)
    to_json("NT-15_1-Timothy", bible_map)
    to_json("NT-16_2-Timothy", bible_map)
    to_json("NT-17_Titus", bible_map)
    to_json("NT-18_Philemon", bible_map)
    to_json("NT-19_Hebrews", bible_map)
    to_json("NT-20_James", bible_map)
    to_json("NT-21_1-Peter", bible_map)
    to_json("NT-22_2-Peter", bible_map)
    to_json("NT-23_1-John", bible_map)
    to_json("NT-24_2-John", bible_map)
    to_json("NT-25_3-John", bible_map)
    to_json("NT-26_Jude", bible_map)
    to_json("NT-27_Revelation", bible_map)

    end_time = time.time()

    total_time = (end_time - start_time) * 1000  # Convert to milliseconds

    print(f"Finished encoding CPDV Bible into JSON format - {total_time:.0f}ms")

    json_str = json.dumps(bible_map, indent=4, ensure_ascii=False)
    file_json = "cpdv-json/EntireBible-CPDV.json"
    with open(file_json, "w", encoding="utf-8") as f:
        f.write(json_str)

