# -*- coding: utf-8 -*-
from scripts._commons_pick import first_working

FIX = [
    ("griffith", "Griffith Observatory Los Angeles building"),
    ("getty_villa", "Getty Villa museum building"),
    ("sg_clarke2", "Clarke Quay Singapore waterfront"),
]
if __name__ == "__main__":
    for k, q in FIX:
        print(k, "->", first_working(q))
