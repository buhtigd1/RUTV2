#!/usr/bin/env python3

import requests

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


def clean_playlist(content: str) -> str:
    lines = []

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#EXTINF"):
            # Keep only channel name, remove all attributes
            if "," in line:
                channel_name = line.split(",", 1)[1].strip()
                line = f"#EXTINF:-1,{channel_name}"
            else:
                line = "#EXTINF:-1"

        lines.append(line)

    if not lines or not lines[0].startswith("#EXTM3U"):
        lines.insert(0, "#EXTM3U")

    return "\n".join(lines) + "\n"


def main():
    playlist = fetch_playlist()
    playlist = clean_playlist(playlist)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
