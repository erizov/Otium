# Whitelist sources (Prague)

As for Smolensk / SPB: new objects should use URLs from listed hosts or
Commons. **`https://upload.wikimedia.org/...`** and
**`https://commons.wikimedia.org/...`** are always allowed (see
`prague/whitelist.py`).

---

## A. Official and cultural portals

| URL | Use |
|-----|-----|
| https://www.praha.eu/ | City administration |
| https://www.prague.eu/ | Visitor portal |

---

## B. Encyclopedias and Commons

| URL | Use |
|-----|-----|
| https://en.wikipedia.org/wiki/ | Articles (`/wiki/...` only) |
| https://cs.wikipedia.org/wiki/ | Czech Wikipedia (`/wiki/...`) |
| https://upload.wikimedia.org/wikipedia/commons/ | Commons files |

Add new `https://...` prefixes here before using them in `image_source_url`
outside Commons.
