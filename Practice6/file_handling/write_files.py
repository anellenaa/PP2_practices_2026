"""Practice 6 - Writing files.
Covers: modes w / a / x, with-statement, write list to file, generate A.txt..Z.txt
"""
import os
import string

BASE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(BASE, "sample.txt")


# 1. Create a text file and write sample data (mode "w")
def create_sample():
    with open(SAMPLE, "w", encoding="utf-8") as f:
        f.write("Hello, Python!\n")
        f.write("This is the second line.\n")
        f.write("File handling is easy.\n")
    print("Created:", SAMPLE)


# 3. Append new lines (mode "a") and verify content
def append_lines():
    with open(SAMPLE, "a", encoding="utf-8") as f:
        f.write("Appended line 1\n")
        f.write("Appended line 2\n")
    with open(SAMPLE, "r", encoding="utf-8") as f:
        print("--- After append ---")
        print(f.read())


# Mode "x": create only if file does not exist, otherwise FileExistsError
def exclusive_create():
    path = os.path.join(BASE, "exclusive.txt")
    try:
        with open(path, "x", encoding="utf-8") as f:
            f.write("Created with mode x\n")
        print("exclusive.txt created")
    except FileExistsError:
        print("exclusive.txt already exists (mode 'x' refused to overwrite)")


# Ex.5: write a list to a file
def write_list_to_file(items, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for item in items:
            f.write(f"{item}\n")
    print(f"Wrote {len(items)} items to {filename}")


# Ex.6: generate 26 text files A.txt ... Z.txt
def generate_alphabet_files(folder):
    os.makedirs(folder, exist_ok=True)
    for letter in string.ascii_uppercase:
        with open(os.path.join(folder, f"{letter}.txt"), "w", encoding="utf-8") as f:
            f.write(f"This is file {letter}.txt\n")
    print(f"Generated {len(string.ascii_uppercase)} files in {folder}")


if __name__ == "__main__":
    create_sample()
    append_lines()
    exclusive_create()
    write_list_to_file(["apple", "banana", "cherry", "date"],
                       os.path.join(BASE, "list_output.txt"))
    generate_alphabet_files(os.path.join(BASE, "alphabet"))
