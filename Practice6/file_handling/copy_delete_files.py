"""Practice 6 - Copy, back up and delete files.
Covers: shutil.copy, copying contents, backups, safe delete with checks
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))


def make_source(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Line 1\nLine 2\nLine 3\n")


# 4. Copy and back up files using shutil
def backup_file(src):
    backup_dir = os.path.join(BASE, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    dst = os.path.join(backup_dir, os.path.basename(src) + ".bak")
    shutil.copy2(src, dst)          # copy2 also keeps metadata
    print("Backup created:", dst)
    return dst


# Ex.7: copy the contents of a file to another file (manually)
def copy_contents(src, dst):
    with open(src, "r", encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Contents of {os.path.basename(src)} copied to {os.path.basename(dst)}")


# 5 + Ex.8: delete a file safely (check existence and access first)
def safe_delete(path):
    if not os.path.exists(path):
        print("Path does not exist:", path)
        return False
    if not os.path.isfile(path):
        print("Not a file:", path)
        return False
    if not os.access(path, os.W_OK):
        print("No write access:", path)
        return False
    os.remove(path)
    print("Deleted:", path)
    return True


if __name__ == "__main__":
    src = os.path.join(BASE, "source.txt")
    copy_target = os.path.join(BASE, "source_copy.txt")

    make_source(src)
    backup_file(src)
    copy_contents(src, copy_target)

    safe_delete(copy_target)
    safe_delete(copy_target)                       # already gone -> message
    safe_delete(os.path.join(BASE, "backup", "source.txt.bak"))
    safe_delete(src)
