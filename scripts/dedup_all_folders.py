#!pip install pillow imagehash

import os
import shutil
import sys
from pathlib import Path

from PIL import Image
import imagehash
from itertools import combinations

# ---------------- CONFIG ----------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.guide_constants import get_images_root

ROOT_DIR = os.environ.get("EXCURSION_IMAGES_ROOT", str(get_images_root()))
PHASH_THRESHOLD = 7            # 6–8 recommended
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

# ----------------------------------------

class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)

    def groups(self):
        clusters = {}
        for item in self.parent:
            root = self.find(item)
            clusters.setdefault(root, []).append(item)
        return list(clusters.values())


def get_images_in_folder(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]


def get_resolution(path):
    try:
        with Image.open(path) as img:
            return img.width * img.height
    except:
        return 0


def ensure_duplicates_folder(folder_path):
    dup_path = os.path.join(folder_path, "duplicates")
    os.makedirs(dup_path, exist_ok=True)
    return dup_path


def move_file_safe(src_path, dst_folder):
    filename = os.path.basename(src_path)
    dst_path = os.path.join(dst_folder, filename)

    # Avoid overwriting
    counter = 1
    while os.path.exists(dst_path):
        name, ext = os.path.splitext(filename)
        dst_path = os.path.join(dst_folder, f"{name}_{counter}{ext}")
        counter += 1

    shutil.move(src_path, dst_path)


def process_folder(folder_path):
    print(f"\nProcessing folder: {folder_path}")

    image_paths = get_images_in_folder(folder_path)

    if len(image_paths) < 2:
        print("Not enough images.")
        return

    print(f"Images found: {len(image_paths)}")

    # -------- Compute pHash --------
    phashes = {}
    for path in image_paths:
        try:
            with Image.open(path) as img:
                phashes[path] = imagehash.phash(img.convert("RGB"))
        except Exception as e:
            print(f"Skipping {path}: {e}")

    # -------- Compare inside folder --------
    uf = UnionFind(list(phashes.keys()))

    for a, b in combinations(phashes.keys(), 2):
        if phashes[a] - phashes[b] <= PHASH_THRESHOLD:
            uf.union(a, b)

    clusters = [c for c in uf.groups() if len(c) > 1]

    print(f"Duplicate clusters found: {len(clusters)}")

    if not clusters:
        return

    duplicates_folder = ensure_duplicates_folder(folder_path)

    # -------- Move duplicates --------
    for cluster in clusters:
        # Keep highest resolution image
        best = max(cluster, key=get_resolution)

        print("\nCluster:")
        for img in cluster:
            print(" ", img)

        print(f"Keeping: {best}")

        for img in cluster:
            if img != best:
                print(f"Moving: {img}")
                move_file_safe(img, duplicates_folder)


def main():
    subfolders = [
        os.path.join(ROOT_DIR, d)
        for d in os.listdir(ROOT_DIR)
        if os.path.isdir(os.path.join(ROOT_DIR, d))
    ]

    print(f"Found {len(subfolders)} folders")

    for folder in subfolders:
        process_folder(folder)


if __name__ == "__main__":
    main()