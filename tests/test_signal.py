import unittest


class SignalTest(unittest.TestCase):

	# Built in test case method (like Before)
	def setUp(self) -> None:
		super().setUp()

	# Built in test case method (like After)
	def tearDown(self) -> None:
		super().tearDown()

	def test_one(self):
		sum_of_things = 1 + 1
		self.assertEqual(2, sum_of_things)

	# Will skip the unit test and has a message explaining why
	# @unittest.skip("WIP")
	def test_two(self):
		sum_of_things = 2 + 2
		self.assertEqual(4, sum_of_things)
