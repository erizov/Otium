# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "moscow" / "data" / "osobnjaki_batch2.py"
for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    if "name_en" in line or "history_en" in line or "significance_en" in line:
        continue
    if ".jpg" in line or line.strip().startswith(("def ", "from ", "import")):
        continue
    latin = [c for c in line if ord(c) < 128 and c.isalpha()]
    if latin and any("\u0400" <= c <= "\u04ff" for c in line):
        print("{}: {}".format(i, line.encode("unicode_escape").decode()))
