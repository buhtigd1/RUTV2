#!/usr/bin/env python3

import requests
from transliterate import translit

SOURCE_URL = "https://raw.githubusercontent.com/Rafail1082GitHUB/rafail1982.ru/main/RUTUBE.m3u8"
OUTPUT_FILE = "rutv2.m3u"


def fetch_playlist() -> str:
    r = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    r.raise_for_status()
    return r.text


def translate_name(name: str) -> str:
    try:
        return translit(name, "ru", reversed=True)
    except Exception:
        return name


def clean_playlist(content: str) -> str:
    output = []

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#EXTINF") and "," in line:
            prefix, channel_name = line.split(",", 1)
            line = f"{prefix},{translate_name(channel_name)}"

        output.append(line)

    return "\n".join(output) + "\n"


def main():
    playlist = fetch_playlist()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(clean_playlist(playlist))

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
``
