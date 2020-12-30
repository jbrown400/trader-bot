from datetime import datetime
from datetime import timedelta

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
