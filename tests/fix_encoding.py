from pathlib import Path

parent = Path(__file__).resolve().parent.parent

safe_path = parent / "randfacts" / "safe.txt"
unsafe_path = parent / "randfacts" / "unsafe.txt"

bad_characters = [
    ("‘", "'"),
    ("’", "'"),
    ("“", '"'),
    ("”", '"'),
    ("…", "..."),
    ("—", "-"),
]

with open(safe_path, "r+", encoding="utf-8") as f:
    safe = f.read()

    for char in bad_characters:
        safe = safe.replace(char[0], char[1])

    f.seek(0)
    f.write(safe)

with open(unsafe_path, "r+", encoding="utf-8") as f:
    unsafe = f.read()

    for char in bad_characters:
        unsafe = unsafe.replace(char[0], char[1])

    f.seek(0)
    f.write(unsafe)
