#!/usr/bin/env python3

# This python script is used to convert the Catholic Public Domain Bible (CPDV) into JSON format.
# Please read the README.md file for more information.
# 
# https://github.com/yoarikso/cpdv_json
# 

import json
import os
import time
import urllib.request


def download(address):
    filename = address.split("/")[-1]
    urllib.request.urlretrieve(address, filename)


def to_json(book_name, bible_map):
    download(to_url(book_name))

    file_html = f"{book_name}.htm"

    with open(file_html, "r", encoding="windows-1252", newline='') as f:
        genesis = f.read()

    results = genesis.split("\r\n")

    book = {}

    for it in results:
        try:
            if it.startswith("{"):
                end_meta = it.index("}")
                meta = it[0:end_meta+1]

                strt_idx = end_meta + 2

                it = it.replace("<BR>", "")
                end_idx = len(it) - 1
                content = it[strt_idx:end_idx]

                # Convert content to UTF-8 (matching Groovy's encode/decode cycle)
                # In Python, strings are Unicode, so we encode to UTF-8 bytes and decode back
                # to match the Groovy behavior of ensuring UTF-8 encoding
                content_utf8 = content.encode("utf-8").decode("utf-8")

                chapter = meta[1:meta.index(":")]
                verse = meta[meta.index(":")+1:meta.index("}")]

                if chapter not in book:
                    book[chapter] = {}

                chapter_map = book[chapter]
                chapter_map[verse] = content_utf8

        except Exception as e:
            print(e)

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

    return f"{host}{book_name}.htm"


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
to_json("OT-24_Song2", bible_map)
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

# New Testament
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
file_json = "CPDV-JSON/EntireBible-CPDV.json"
with open(file_json, "w", encoding="utf-8") as f:
    f.write(json_str)

