import os

parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

safe_path = os.path.join(parent, 'safe.txt')
unsafe_path = os.path.join(parent, 'unsafe.txt')

with open(safe_path, encoding="utf-8") as f:
	safe = f.read()
	
safe = safe.replace("‘", "'")
safe = safe.replace("’", "'")
safe = safe.replace("“", '"')
safe = safe.replace("”", '"')
with open(safe_path, "w") as f:
	f.write(safe)
	
with open(unsafe_path, encoding="utf-8") as f:
	unsafe = f.read()
	
unsafe = unsafe.replace("‘", "'")
unsafe = unsafe.replace("’", "'")
unsafe = unsafe.replace("“", '"')
unsafe = unsafe.replace("”", '"')
with open(unsafe_path, "w") as f:
	f.write(unsafe)