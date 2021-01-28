import randfacts

print("")
print("")
print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[36mInitializing test! (1/1)")
try:
	print(u"\u001b[33m===================================================================\u001b[0m")
	print(randfacts.getFact())
	print(u"\u001b[33m===================================================================\u001b[0m")
	print("")
except AttributeError:
	print(u"\u001b[31m===================================================================\u001b[0m")
	print(u"\u001b[31mWhoops! Executing a getFact() call got an error!\u001b[0m")
	print(u"\u001b[31m===================================================================\u001b[0m")
	exit(2)
print(u"\u001b[33m===================================================================\u001b[0m")
print(u"\u001b[32mSuccessful Test! (1/1 COMPLETE)\u001b[0m")
print(u"\u001b[35mTerminating!\u001b[0m")
print(u"\u001b[33m===================================================================\u001b[0m")
exit()
