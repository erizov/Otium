# -*- coding: utf-8 -*-
"""One-off resolver: print upload.wikimedia.org URLs for city guide files."""
import json
import sys
import urllib.parse
import urllib.request


def url(title: str) -> str | None:
    t = title if title.startswith("File:") else "File:" + title
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": t,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }
    )
    req = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + q,
        headers={"User-Agent": "ExcursionGuide-batch/1.0"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        d = json.load(resp)
    for p in d["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]
    return None


def main(argv: list[str]) -> None:
    for raw in argv[1:]:
        u = url(raw)
        print("{}\t{}".format(raw, u or "MISS"))


if __name__ == "__main__":
    main(sys.argv)
