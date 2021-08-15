import unittest
import sys
import pathlib
import subprocess

sys.path.insert(1, str(pathlib.Path(__file__).parents[1]))
from randfacts import randfacts # local randfacts instead of installed version

class TestRandfacts(unittest.TestCase):

	def test_get_fact(self):
		self.assertIsInstance(randfacts.get_fact(), str, 'get_fact() must return a string')

	def test_all_facts_list(self):
		self.assertIsInstance(randfacts.all_facts, list, 'all_facts must be a list')

	def test_safe_facts_list(self):
		self.assertIsInstance(randfacts.safe_facts, list, 'safe_facts must be a list')

	def test_unsafe_facts_list(self):
		self.assertIsInstance(randfacts.unsafe_facts, list, 'unsafe_facts must be a list')

	def test_cli_no_args(self):
		child = subprocess.Popen(['python3', '-m', 'randfacts'], stdout=subprocess.DEVNULL)
		child.communicate()
		self.assertEqual(child.returncode, 0, '`python3 -m randfacts` must return with exit code 0')

	def test_cli_unsafe_args(self):
		child = subprocess.Popen(['python3', '-m', 'randfacts', '--unsafe'], stdout=subprocess.DEVNULL)
		child.communicate()
		self.assertEqual(child.returncode, 0, '`python3 -m randfacts --unsafe` must return with exit code 0')

	def test_cli_mixed_args(self):
		child = subprocess.Popen(['python3', '-m', 'randfacts', '--mixed'], stdout=subprocess.DEVNULL)
		child.communicate()
		self.assertEqual(child.returncode, 0, '`python3 -m randfacts --mixed` must return with exit code 0')

	def test_invalid_characters(self):
		bad_characters = ["‘", "’", "“", "”", "…", "—"]
		for index, fact in enumerate(randfacts.all_facts):
			for char in bad_characters:
				self.assertNotIn(char, fact, f'Index: {index}')

if __name__ == '__main__':
	unittest.main()