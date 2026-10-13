"""Practice 6 - Move / copy files between directories using shutil and pathlib."""
import os
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = BASE / "move_demo" / "source"
DST = BASE / "move_demo" / "destination"


def prepare():
    SRC.mkdir(parents=True, exist_ok=True)
    DST.mkdir(parents=True, exist_ok=True)
    for name in ["one.txt", "two.txt", "three.py"]:
        (SRC / name).write_text(f"content of {name}\n", encoding="utf-8")


def copy_files():
    shutil.copy(SRC / "one.txt", DST / "one_copy.txt")
    print("Copied one.txt ->", DST / "one_copy.txt")


def move_files():
    shutil.move(str(SRC / "two.txt"), str(DST / "two.txt"))
    print("Moved two.txt ->", DST / "two.txt")


def move_by_extension(ext):
    """Move every file with the given extension from SRC to DST."""
    for p in SRC.iterdir():
        if p.is_file() and p.suffix == ext:
            shutil.move(str(p), str(DST / p.name))
            print("Moved", p.name)


def show(folder):
    print(folder.name, "->", sorted(os.listdir(folder)))


if __name__ == "__main__":
    prepare()
    copy_files()
    move_files()
    move_by_extension(".py")
    show(SRC)
    show(DST)
