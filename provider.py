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
    lines = ["#EXTM3U"]  # Clean header

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        # Skip original header completely
        if line.startswith("#EXTM3U"):
            continue

        # Remove all EXTINF attributes
        if line.startswith("#EXTINF"):
            if "," in line:
                channel_name = line.split(",", 1)[1].strip()
                line = f"#EXTINF:-1,{channel_name}"
            else:
                continue

        lines.append(line)

    return "\n".join(lines) + "\n"


def main():
    playlist = fetch_playlist()
    playlist = clean_playlist(playlist)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
