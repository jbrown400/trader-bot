from datetime import datetime
from datetime import timedelta
import pandas as pd

from pyrobot.robot import PyRobot


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def print_step(trading_robot: PyRobot, indicator_client):
	# Check for the signals
	signals = indicator_client.check_signals()

	print("=" * 50)
	print("Ownership Status: {}".format(trading_robot.portfolio.positions))
	print("Current Signals: ")
	print("Buy signals: {}".format(signals['buys'].to_list()))
	print("Sell Signals: {}".format(signals['sells'].to_list()))
	print(trading_robot.portfolio.stock_frame.symbol_groups.tail(n=3))
	print("-" * 50)
	print("")


def set_historical_prices(trading_robot: PyRobot):
	"""
		Set the historical prices for the robot

		Arguments:
			trading_robot {PyRobot} -- The trading robot class
	"""

	end_date = datetime.today()
	start_date = end_date - timedelta(days=20)

	# Get historical data
	historical_prices = trading_robot.grab_historical_prices(
		start=start_date,
		end=end_date,
		bar_size=1,
		bar_type='minute'
	)

	# Convert data to a stock frame
	stock_frame = trading_robot.create_stock_frame(
		data=historical_prices['aggregated']
	)

	# Add the stock frame to the portfolio
	trading_robot.portfolio.stock_frame = stock_frame
	trading_robot.portfolio.historical_prices = historical_prices


def set_trade(trading_robot: PyRobot, trading_symbol: str,
              max_percent: float,
              current_price: int,
              available_funds) -> dict:
	"""
	Create order legs and set the qty based on how much of my portfolio
	  I want to trade at one time
	:param trading_robot: the robot
	:param trading_symbol: the ticker symbol for the trades
	:param max_percent: max percentage of my portfolio I want for a single trade
	:param current_price: current candle open price
	:param available_funds: current amount I can trade with
	:return: trade dictionary
	"""

	qty = round((available_funds * max_percent) / current_price) if max_percent is not None else 1

	new_enter_trade = trading_robot.create_trade(
		trade_id='long_enter',
		enter_or_exit='enter',
		long_or_short='long',
		order_type='mkt'
	)

	# Add an Order Leg
	new_enter_trade.instrument(
		symbol=trading_symbol,
		quantity=qty,
		asset_type='EQUITY'
	)

	# Create a new Trade Object for Exiting position
	new_exit_trade = trading_robot.create_trade(
		trade_id='long_exit',
		enter_or_exit='exit',
		long_or_short='long',
		order_type='mkt'
	)

	# Add an Order Leg
	new_exit_trade.instrument(
		symbol=trading_symbol,
		quantity=qty,
		asset_type='EQUITY'
	)

	return {
		trading_symbol: {
			'buy': {
				'trade_func': trading_robot.trades['long_enter'],
				'trade_id': trading_robot.trades['long_enter'].trade_id
			},
			'sell': {
				'trade_func': trading_robot.trades['long_exit'],
				'trade_id': trading_robot.trades['long_exit'].trade_id
			},
		}
	}