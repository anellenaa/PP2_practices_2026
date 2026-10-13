# Practice 6 — File Handling, Directory Management, Built-in Functions

## Structure
```
Practice6/
├── file_handling/
│   ├── read_files.py          # r, read(), readline(), readlines(), count lines
│   ├── write_files.py         # w, a, x, write list, generate A.txt..Z.txt
│   └── copy_delete_files.py   # shutil copy/backup, copy contents, safe delete
├── directory_management/
│   ├── create_list_dirs.py    # mkdir/makedirs/listdir/chdir/getcwd/rmdir, access, path info, find by ext
│   └── move_files.py          # move/copy between directories (shutil, pathlib)
├── builtin_functions/
│   ├── map_filter_reduce.py   # len/sum/min/max/sorted, map, filter, reduce
│   └── enumerate_zip_examples.py  # enumerate, zip, type checks & conversions
└── README.md
```

## Run
```
python file_handling/write_files.py
python file_handling/read_files.py
python file_handling/copy_delete_files.py
python directory_management/create_list_dirs.py
python directory_management/move_files.py
python builtin_functions/map_filter_reduce.py
python builtin_functions/enumerate_zip_examples.py
```

## Exercise mapping
| Task | File |
|---|---|
| File 1–3 (create, read, append) | write_files.py, read_files.py |
| File 4–5 (shutil copy/backup, delete) | copy_delete_files.py |
| Dir 1–4 | create_list_dirs.py, move_files.py |
| Built-in 1–4 | map_filter_reduce.py, enumerate_zip_examples.py |
| Combined 1 (list dirs/files) | create_list_dirs.py → list_path, list_all_recursive |
| Combined 2 (access) | create_list_dirs.py → check_access |
| Combined 3 (path exists, filename/dir) | create_list_dirs.py → path_info |
| Combined 4 (count lines) | read_files.py → count_lines |
| Combined 5 (write list) | write_files.py → write_list_to_file |
| Combined 6 (A.txt..Z.txt) | write_files.py → generate_alphabet_files |
| Combined 7 (copy contents) | copy_delete_files.py → copy_contents |
| Combined 8 (delete with checks) | copy_delete_files.py → safe_delete |
