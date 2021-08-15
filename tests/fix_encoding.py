import os

parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

safe_path = os.path.join(parent, 'randfacts', 'safe.txt')
unsafe_path = os.path.join(parent, 'randfacts', 'unsafe.txt')

bad_characters = [("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("…", "..."), ('—', '-')]

with open(safe_path, encoding="utf-8") as f:
	safe = f.read()

for char in bad_characters:
	safe = safe.replace(char[0], char[1])

with open(safe_path, "w") as f:
	f.write(safe)

with open(unsafe_path, encoding="utf-8") as f:
	unsafe = f.read()

for char in bad_characters:
	unsafe = unsafe.replace(char[0], char[1])

with open(unsafe_path, "w") as f:
	f.write(unsafe)