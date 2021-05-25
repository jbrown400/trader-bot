from pyrobot.robot import PyRobot

from core.finnhub.finnhub import Finnhub
from core.robot import Agent

# todo do I want multiple robots and pit them against each other?
#  yes...so do adversarial training and then pick the best one each month..?


class Robot(PyRobot):
	"""
	Extends PyRobot class (which contains TD API) to add functionality or quickly implement bug fixes
	"""

	def __init__(self, client_id: str, redirect_uri: str, paper_trading: bool = True, credentials_path: str = None,
	             trading_account: str = None):
		super().__init__(client_id, redirect_uri, paper_trading, credentials_path, trading_account)
		self.py_robot = PyRobot(client_id, redirect_uri, paper_trading, credentials_path, trading_account)
		self.tickers = []
		#todo uhhh idk if I need to store all data in one table or each ticker in its own table...
		self.db_table_names = ['rawData', 'processedData', 'models']
		self.agent: Agent = None

	@property
	def agent(self):
		"""
		Think of the agent like the "brain" of the Robot

		:return: The trained agent that will choose the actions.
		"""
		return self.agent

	@agent.setter
	def agent(self, value: Agent):
		self._agent = value

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

	def get_today_data(self):
		"""
		#todo make this run daily after 8pm CST (no more trading)
		This will pull the most recent day's data, clean it, and save it for later training
		(probs pull from both TD and Finnhub)
		#todo should I put pre, regular, and post market data in different tables...?
		:return:
		"""
		pass

	def open_real_time_data_connection(self):
		"""
		Opens a web socket for the ticker the bot is focused on
		#todo don't forget to close it when done
		:return:
		"""
		pass

	def prep_new_ticker(self):
		"""
		Starts and manages preparing everything we need to do when we see a new ticker we want to trade
		:return:
		"""
		pass

	def get_historical_finnhub_data(self, ticker: str):
		Finnhub.get_historical_data(ticker)
		# todo send to cleaner

