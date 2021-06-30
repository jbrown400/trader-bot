import unittest


class SignalTest(unittest.TestCase):

	def test_one(self):
		sum_of_things = 1 + 1
		self.assertEqual(2, sum_of_things)

	def test_two(self):
		sum_of_things = 2 + 2
		self.assertEqual(4, sum_of_things)