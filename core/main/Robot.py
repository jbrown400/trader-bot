from pyrobot.robot import PyRobot

#todo do I want multiple robots and pit them against each other?
# yes...so do adversarial training and then pick the best one each month..?

class Robot:
	"""
	Extends PyRobot class (which contains TD API) to add functionality or quickly implement bug fixes
	"""

	def __init__(self, client_id: str,
	             redirect_uri: str,
	             paper_trading: bool = True,
	             credentials_path: str = None,
	             trading_account: str = None):
		self.py_robot = PyRobot(client_id, redirect_uri, paper_trading, credentials_path, trading_account)
		self.tickers = []

	@property
	def tickers(self):
		return self.tickers

	@tickers.setter
	def tickers(self, value):
		self._tickers = value

	@property
	def performance(self):
		"""
		Calculate and return current performance metrics...not really sure what that metric will be tho...
		:return: Performance metric
		"""
		return "performance"
