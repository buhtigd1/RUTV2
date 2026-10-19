#!/usr/bin/env python3

import re
import requests
from transliterate import translit

SOURCE_URL = "https://raw.githubusercontent.com/Rafail1082GitHUB/rafail1982.ru/main/RUTUBE.m3u8"
OUTPUT_FILE = "rutv2.m3u"


def fetch_playlist() -> str:
    response = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()
    return response.text


def transliterate_text(text: str) -> str:
    try:
        return translit(text, "ru", reversed=True)
    except Exception:
        return text


def clean_extinf(line: str) -> str:
    # Remove metadata
    line = re.sub(r'\s*group-title="[^"]*"', "", line)
    line = re.sub(r'\s*tvg-id="[^"]*"', "", line)
    line = re.sub(r'\s*tvg-name="[^"]*"', "", line)

    # Transliterate channel name
    if "," in line:
        prefix, channel_name = line.rsplit(",", 1)
        channel_name = transliterate_text(channel_name.strip())
        line = f"{prefix},{channel_name}"

    return line


def clean_playlist(content: str) -> str:
    result = ["#EXTM3U"]

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        # Replace source header
        if line.startswith("#EXTM3U"):
            continue

        if line.startswith("#EXTINF"):
            line = clean_extinf(line)

        result.append(line)

    return "\n".join(result) + "\n"


def main():
    playlist = fetch_playlist()
    cleaned = clean_playlist(playlist)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(cleaned)

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
