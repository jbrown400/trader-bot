import sys
from datetime import datetime
from datetime import timedelta

import psycopg2
from pyrobot.indicators import Indicators
from pyrobot.robot import PyRobot
from pyrobot.stock_frame import StockFrame

import utils.general_utils as util
from configs.config import *
from models.enums.Duration import Duration
from network.finnhub.finnhub import Finnhub
from robot import Agent
from strategies import conf_val


# todo do I want multiple robots and pit them against each other?
#  yes...so do adversarial training and then pick the best one each month..?


class Robot(PyRobot):
	"""
	Extends PyRobot class (which contains TD API) to add functionality or quickly implement bug fixes
	"""

	def __init__(self, client_id: str, redirect_uri: str, paper_trading: bool = True,
	             credentials_path: str = None, ticker: str = 'PLTR', trading_account: str = None):
		super().__init__(client_id, redirect_uri, paper_trading, credentials_path, trading_account)
		"""*** Properties*** """
		self.py_robot = PyRobot(client_id, redirect_uri, paper_trading, credentials_path, trading_account)
		self.tickers = ticker
		self._agent: Agent = None
		self._trades_dict = {}
		self._ownership_dict = {}
		# self._indicator_client: Indicators = None
		self._signals = dict
		# Actions
		self.create_portfolio()
		# self.define_enter_and_exit_trades(ticker)
		self.set_ownership_dict(ticker)



	# self.portfolio.add_position(symbol='PLTR', quantity=1, asset_type='equity')
	# self.get_data('TDA', tickers=self.tickers)

	@property
	def agent(self):
		"""
		Think of the agent like the "brain" of the Robot

		:return: The trained agent that will choose the actions.
		"""
		return self._agent

	@agent.setter
	def agent(self, value: Agent):
		self._agent = value

	@property
	def tickers(self):
		return self._tickers

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

	def define_enter_and_exit_trades(self, ticker):

		available_funds = self.get_accounts(account_number=ACCOUNT_NUMBER)[0]['cash_available_for_trading']
		max_percent = .1  # 10%
		current_price = self._indicator_client.price_data_frame['open'][0]
		qty = round((available_funds * max_percent) / current_price) if max_percent else 1

		# Create trade object for entering position
		new_enter_trade = self.create_trade(
			trade_id='long_enter',
			enter_or_exit='enter',
			long_or_short='long',
			order_type='mkt'
		)
		# Add an order leg for the enter trade
		new_enter_trade.instrument(
			symbol=ticker,
			quantity=qty,
			asset_type='EQUITY'
		)
		# Create a new trade object for exiting position
		new_exit_trade = self.create_trade(
			trade_id='long_exit',
			enter_or_exit='exit',
			long_or_short='long',
			order_type='mkt'
		)
		# Add an order leg for the exit trade
		new_exit_trade.instrument(
			symbol=ticker,
			quantity=qty,
			asset_type='EQUITY'
		)

		self._trades_dict = {
			ticker: {
				'buy': {
					'trade_func': self.trades['long_enter'],
					'trade_id': self.trades['long_enter'].trade_id
				},
				'sell': {
					'trade_func': self.trades['long_exit'],
					'trade_id': self.trades['long_exit'].trade_id
				},
			}
		}

	def set_ownership_dict(self, ticker):
		self._ownership_dict = {
			ticker: False
		}

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

	def get_and_process_data(self, tickers: [str]):
		# Pull data
		# self.get_data('TDA', tickers=tickers)
		# Clean data
		# Todo implement data cleaning
		# Store data
		end_date = datetime.today()

		start_date = end_date - timedelta(days=20)

		# Get historical data
		historical_prices = self.grab_historical_prices(
			start=start_date,
			end=end_date,
			bar_size=1,
			bar_type='minute'
		)
		# todo clean data
		# Create stock frame
		self.portfolio.stock_frame = self.create_stock_frame(data=historical_prices['aggregated'])
		# Fill in missing values
		# todo fill in missing values

		# Calculate MACD, RSI, and VWAP
		self._indicator_client = Indicators(price_data_frame=self.portfolio.stock_frame)
		conf_val.calculate_columns(self._indicator_client, owned=False, trading_symbol=self._tickers[0],
		                           bot_account=self.get_accounts(account_number=ACCOUNT_NUMBER))

		# todo insert signals data into a column on stock frame

		# Insert into db
		self.insert_into_db(table=tickers[0],
		                    stock_frame=self.portfolio.stock_frame)

	def get_historical_finnhub_data(self, ticker: str):
		Finnhub.get_historical_data(ticker)

	def initialize_db(self):
		#todo remove this as the robot should not house the db. It should interact with whichever
		#  db is in the environment
		self.db_connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

	def insert_into_db(self, table: str, stock_frame: StockFrame):
		try:
			cursor = self.db_connection.cursor()
			# create table
			create_command = f"""
					CREATE TABLE IF NOT EXISTS {table} (
						time_stamp TIMESTAMP NOT NULL PRIMARY KEY,
						open NUMERIC NOT NULL,
						close NUMERIC NOT NULL,
						high NUMERIC NOT NULL,
						low NUMERIC NOT NULL,
						volume NUMERIC NOT NULL,
						ema_20 NUMERIC NOT NULL,
						ema_200 NUMERIC NOT NUll,
						macd NUMERIC NOT NULL,
						rsi NUMERIC NOT NULL,
						open_ema_20_percent_diff NUMERIC NOT NULL,
						ema_20_ema_200_percent_diff NUMERIC NOT NULL,
						prev_owned BOOLEAN NOT NULL,
						signal TEXT NOT NULL,
						account_value NUMERIC NOT NULL
					)
					"""
			cursor.execute(create_command)
			# print(historical_prices)
			# start with the first ticker
			for index, row in stock_frame.frame.iterrows():
				# timestamp = str(datetime.fromtimestamp(index[1].value//1000.0))
				insert_command = f"""
					INSERT INTO {table} (time_stamp, open, close, high, low, volume, ema_20, ema_200, macd, rsi,
											open_ema_20_percent_diff, ema_20_ema_200_percent_diff, prev_owned, signal,
											account_value)
								values ('{index[1]}',
										{row['open']},
										{row['close']},
										{row['high']},
										{row['low']},
										{row['volume']},
										{row['ema_20']},
										{row['ema_200']},
										{row['macd']},
										{row['rsi']},
										{row['open_ema_20_percent_diff']},
										{row['ema_20_ema_200_percent_diff']},
										'{row['prev_owned']}',
										'{row['signal']}',
										{row['account_value']}) ON CONFLICT (time_stamp) DO UPDATE
										SET signal = EXCLUDED.signal
					"""
				cursor.execute(insert_command)
			# stock_frame.to_sql(table, )
			self.db_connection.commit()
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')
			sys.exit(1)
		finally:
			pass
			# if self.db_connection:
			# 	self.db_connection.close()

	def select_from_db(self):
		pass

	def paper_trading(self):
		# Select strat

		# Open data stream
		while self.regular_market_open:
			latest_bar = self.get_latest_bar()  # Read in minute candle
			self.portfolio.stock_frame.add_rows(data=latest_bar)  # Save to in memory df
			# todo save latest_bar to db

		# while stream is connected and market is open
		"""
			1. Read in minute candle
			2. Store candle data into DB
			3. Store candle data into in memory df (should I just store the whole df after market close..?)
				(no, store each candle in case the program crashes and we lose the in memory df)
			4. Using in memory df, calculate signal
		"""

		pass

	def simulate_trading(self, time_period: Duration):
		"""
		For the specified time period, run paper trading and see how much the bot made
		:param time_period:
		:return:
		"""
		current_account_value = 1000
		print("Starting to paper trade")
		for index, row in self.stock_frame.frame.iterrows():
			# Simulate signal
			if row['signal'] == "buy":
				row['own'] = True
				current_account_value -= row['open'] * 10
			elif row['signal'] == "sell":
				row['own'] = False
				current_account_value += row['open'] * 10
			row['account_value'] = current_account_value
		print(current_account_value)
		"""
		try:
			cursor = self.db_connection.cursor()
			select_command = f""
					SELECT * FROM {self._tickers[0]} ORDER BY time_stamp ASC
			""
			cursor.execute(select_command)
			# Need to use fetchone() so I don't try to load all the data in memory
			row = cursor.fetchone()
			while row is not None:
				# Simulate signal
				if row['signal'] == "buy":
					row['own'] = True
					row['account_value'] -= row['open'] * 100
				elif row['signal'] == "sell":
					row['own'] = False
					row['account_value'] += row['open'] * 100
				print(row)
				row = cursor.fetchone()
		except psycopg2.DatabaseError as e:
			print(f'Error {e}')
			sys.exit(1)
		finally:
			if self.db_connection:
				self.db_connection.close()
		"""