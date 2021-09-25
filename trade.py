from pyrobot.indicators import Indicators

from robot.Robot import Robot


def trade(robot: Robot, db, ticker: str, trading_type: str):
	"""
	:param robot: the Robot doing all the computation
	:param db: currently connected db for storing and providing data
	:param ticker: ticker of the stock to trade
	:param trading_type: Simulated, Paper, or Real trading
	:return: None (trading completed)
	"""

	if trading_type == 'simulated':
		# Load data from db into mocked stream
		pass
	else:
		# While market open
		# Open connection to data stream
		pass

	# While market open (or we are going with a simulation)
	while robot.regular_market_open or trading_type == 'simulated':
		latest_bar = robot.get_latest_bar()
		robot.portfolio.stock_frame.add_rows(data=latest_bar)

		indicator_client = Indicators(price_data_frame=robot.portfolio.stock_frame)
		robot.define_enter_and_exit_trades(ticker=ticker)
		indicator_client.refresh()

		signals = ...

		if trading_type == 'paper':
			# execute mock trade
			pass
