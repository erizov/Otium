# Whitelist sources (Budapest)

As for Prague: new objects should use URLs from listed hosts or Commons.
**`https://upload.wikimedia.org/...`** and **`https://commons.wikimedia.org/...`**
are always allowed (see `budapest/whitelist.py`).

---

## A. Official and visitor portals

| URL | Use |
|-----|-----|
| https://www.budapestinfo.hu/ | Visitor information |
| https://budapest.hu/ | Municipality (when linking pages) |

---

## B. Encyclopedias and Commons

| URL | Use |
|-----|-----|
| https://en.wikipedia.org/wiki/ | Articles (`/wiki/...` only) |
| https://hu.wikipedia.org/wiki/ | Hungarian Wikipedia (`/wiki/...`) |
| https://upload.wikimedia.org/wikipedia/commons/ | Commons files |

Add new `https://...` prefixes here before using them in `image_source_url`
outside Commons.
