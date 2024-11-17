"""Fixes common encoding errors that can get into the fact lists after web scraping."""

from pathlib import Path

parent = Path(__file__).resolve().parent.parent

safe_path = parent / "randfacts" / "safe.txt"
unsafe_path = parent / "randfacts" / "unsafe.txt"

bad_characters = [
	("‘", "'"),  # noqa: RUF001
	("’", "'"),  # noqa: RUF001
	("“", '"'),
	("”", '"'),
	("…", "..."),
	("—", "-"),
]

with safe_path.open("r+", encoding="utf-8") as f:
	safe = f.read()

	for char in bad_characters:
		safe = safe.replace(char[0], char[1])

	f.seek(0)
	f.write(safe)

with unsafe_path.open("r+", encoding="utf-8") as f:
	unsafe = f.read()

	for char in bad_characters:
		unsafe = unsafe.replace(char[0], char[1])

	f.seek(0)
	f.write(unsafe)
