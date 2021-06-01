"""
Contains functions for cleaning data retrieved remotely
Note: I think a lot of these actions with be handled by the robot libraries
  but I can perform any extra cleaning steps I need to so everything will
  still be in this file
"""
from models.RawStockRecord import RawStockRecord


def filter_data(raw_data: RawStockRecord):
	"""
	Filters out data that does not need to be saved to any files and send remaining data to be saved/processed
	:param raw_data:
	:return:
	"""
	pass


def fill_in_missing_values(method='mean'):
	"""

	:param method: What to do with missing values (I think)
	:return:
	"""
	pass


def normalize():
	# See if sci-kit or tensorflow can handle this for me
	pass


def standardize():
	pass
