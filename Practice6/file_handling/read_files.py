"""Practice 6 - Reading files.
Covers: mode r, read(), readline(), readlines(), with-statement, counting lines
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(BASE, "sample.txt")


def ensure_sample():
    """Create sample.txt if it does not exist yet."""
    if not os.path.exists(SAMPLE):
        with open(SAMPLE, "w", encoding="utf-8") as f:
            f.write("Hello, Python!\nThis is the second line.\nFile handling is easy.\n")


# 2. Read and print file contents
def read_whole(path):
    with open(path, "r", encoding="utf-8") as f:
        print("read():")
        print(f.read())


def read_line_by_line(path):
    with open(path, "r", encoding="utf-8") as f:
        print("readline():")
        print(repr(f.readline()))   # first line
        print(repr(f.readline()))   # second line


def read_all_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print("readlines():", lines)


# Ex.4: count the number of lines in a text file
def count_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    ensure_sample()
    read_whole(SAMPLE)
    read_line_by_line(SAMPLE)
    read_all_lines(SAMPLE)
    print("Number of lines:", count_lines(SAMPLE))
