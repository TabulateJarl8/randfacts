import randfacts
import os
import re

print("")
print("")
print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[36mInitializing test! (1/3)")
try:
	print(u"\u001b[33m===================================================================\u001b[0m")
	print(randfacts.getFact())
	print(u"\u001b[33m===================================================================\u001b[0m")
	print("")
except AttributeError:
	print(u"\u001b[31m===================================================================\u001b[0m")
	print(u"\u001b[31mWhoops! Executing a getFact() call got an AttributeError!\u001b[0m")
	print(u"\u001b[31m===================================================================\u001b[0m")
	exit(2)
print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[32mSuccessful Test! (1/3 COMPLETE)\u001b[0m")
print(u"\u001b[36mInitializing test! (2/3)\u001b[0m")
try:
	print(u"\u001b[33m===================================================================\u001b[0m")
	print(randfacts.getVersion())

	print(u"\u001b[33m===================================================================\u001b[0m")
	print("")
except AttributeError:
	print(u"\u001b[31m===================================================================\u001b[0m")
	print(u"\u001b[31mWhoops! Executing a getVersion() call got an AttributeError!\u001b[0m")
	print(u"\u001b[31m===================================================================\u001b[0m")
	exit(2)

print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[32mSuccessful Test! (2/3 COMPLETE)\u001b[0m")
print(u"\u001b[36mInitializing test! (3/3)\u001b[0m")

# Check that versions are the same
print(u"\u001b[33m===================================================================\u001b[0m")
try:
	# Get parent directory of directory that test.py is in
	basedir = os.path.dirname(os.path.dirname(__file__))
	# Read setup.py and remove spaces
	with open(os.path.join(basedir, "setup.py")) as f:
		setup = f.read().replace(" ", "")
	# Read main randfacts file and remove spaces
	with open(os.path.join(basedir, "randfacts/main.py")) as f:
		main = f.read().replace(" ", "")
	# Use PEP 440 complient regex to search for version in both files
	setupversion = re.search(r"version=\"(([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?)\"", setup).group(1)
	mainversion = re.search(r"version=\"(([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?)\"", main).group(1)

	# Test if versions are the same
	if setupversion != mainversion:
		print(u"\u001b[31mVersions in setup.py and main.py differ\u001b[0m")
		print(u"\u001b[31m===================================================================\u001b[0m")
		exit(2)
	else:
		print(u"\u001b[32mVersions in setup.py and main.py match\u001b[0m")
		print(u"\u001b[33m===================================================================\u001b[0m")
		print("")
except AttributeError:
	print(u"\u001b[31m===================================================================\u001b[0m")
	print(u"\u001b[31mWhoops! Attempted to check versions! Got a AttributeError!\u001b[0m")
	print(u"\u001b[31m===================================================================\u001b[0m")
	exit(2)
except FileNotFoundError:
	print(u"\u001b[31m===================================================================\u001b[0m")
	print(u"\u001b[31mWhoops! Attempted to check versions! Got a FileNotFoundError!\u001b[0m")
	print(u"\u001b[31m===================================================================\u001b[0m")
	exit(2)

print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[32mSuccessful Test! (3/3 COMPLETE)\u001b[0m")
print(u"\u001b[35mTerminating!\u001b[0m")
print(u"\u001b[33m===================================================================\u001b[0m")
exit()
