"""Practice 6 - Directory management.
Covers: os.mkdir, os.makedirs, os.listdir, os.chdir, os.getcwd, os.rmdir,
        listing dirs/files, access check, path split, find by extension
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "demo_dir")


# 1. Create nested directories
def create_nested():
    os.makedirs(os.path.join(ROOT, "level1", "level2", "level3"), exist_ok=True)
    single = os.path.join(ROOT, "single")
    if not os.path.exists(single):
        os.mkdir(single)
    files = {
        "a.txt": "A",
        "b.py": "print('b')",
        os.path.join("level1", "c.txt"): "C",
        os.path.join("level1", "level2", "d.py"): "print('d')",
    }
    for rel, text in files.items():
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(text)
    print("Nested directories created under", ROOT)


# 2 + Ex.1: list files and folders
def list_path(path):
    items = os.listdir(path)
    dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
    files = [i for i in items if os.path.isfile(os.path.join(path, i))]
    print("All items  :", items)
    print("Only dirs  :", dirs)
    print("Only files :", files)


def list_all_recursive(path):
    """All directories and files in a path (walks subfolders)."""
    for dirpath, dirnames, filenames in os.walk(path):
        print("DIR :", dirpath)
        for name in filenames:
            print("   FILE:", os.path.join(dirpath, name))


# 3. Find files by extension
def find_by_extension(path, ext):
    found = []
    for dirpath, _, filenames in os.walk(path):
        for name in filenames:
            if name.endswith(ext):
                found.append(os.path.join(dirpath, name))
    return found


# Ex.2: check access to a path
def check_access(path):
    print("Path        :", path)
    print("Exists      :", os.access(path, os.F_OK))
    print("Readable    :", os.access(path, os.R_OK))
    print("Writable    :", os.access(path, os.W_OK))
    print("Executable  :", os.access(path, os.X_OK))


# Ex.3: does path exist? if yes -> filename and directory portions
def path_info(path):
    if os.path.exists(path):
        print("Path exists")
        print("Directory portion:", os.path.dirname(path))
        print("Filename portion :", os.path.basename(path))
    else:
        print("Path does not exist")


# chdir / getcwd demo
def cwd_demo():
    old = os.getcwd()
    print("Current dir:", old)
    os.chdir(ROOT)
    print("After chdir:", os.getcwd())
    os.chdir(old)


# rmdir: removes only EMPTY directories
def remove_empty_dir():
    tmp = os.path.join(ROOT, "temp_empty")
    os.mkdir(tmp)
    os.rmdir(tmp)
    print("Empty directory created and removed with os.rmdir")


if __name__ == "__main__":
    create_nested()
    print("\n-- list_path --");   list_path(ROOT)
    print("\n-- os.walk --");     list_all_recursive(ROOT)
    print("\n-- .py files --");   print(find_by_extension(ROOT, ".py"))
    print("\n-- access --");      check_access(ROOT)
    print("\n-- path info --")
    path_info(os.path.join(ROOT, "a.txt"))
    path_info(os.path.join(ROOT, "nope.txt"))
    print("\n-- cwd --");         cwd_demo()
    print("\n-- rmdir --");       remove_empty_dir()
