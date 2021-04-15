import json
import time as time_lib
import pytz
import pprint
import pathlib
import time
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta

from pyrobot.robot import Trade
from pyrobot.indicators import Indicators
from configs.config import *

from typing import List
from typing import Dict

from core.utils.general_utils import *
from core.utils import trade_utils

from strategies import conf_val

from core.finnhub.finnhub import Finnhub

# todo Check if orders were filled (aka I have a position)
#  before trying to sell


if __name__ == '__main__':

	# Hyper parameters
	Finnhub.get_historical_data('AAPL')

	trading_robot = PyRobot(
		client_id=CLIENT_ID,
		redirect_uri=REDIRECT_URI,
		credentials_path=JSON_PATH,
		trading_account=ACCOUNT_NUMBER,
		paper_trading=True
	)

	bot_account = trading_robot.get_accounts(account_number=ACCOUNT_NUMBER)
	pprint.pprint(bot_account)

	print("Pre market open: ", trading_robot.pre_market_open)
	print("Regular market open: ", trading_robot.regular_market_open)
	print("Post market open: ", trading_robot.post_market_open)

	trading_robot_portfolio = trading_robot.create_portfolio()

	trading_symbol = 'CCIV'

	trading_robot_portfolio.add_position(
		symbol=trading_symbol,
		quantity=1,
		asset_type='equity',
	)

	# Set historical prices for current positions
	set_historical_prices(trading_robot)
	# todo create a new dataframe that is cleaned/normalized for the model

	# Create new indicator client
	indicator_client = Indicators(price_data_frame=trading_robot.portfolio.stock_frame)
	# Set the confirmation validation strategy
	conf_val.define_strat(trading_robot, indicator_client)
	pd.set_option('display.max_columns', None)

	# Create a new Trade Object for Entering position
	# new_enter_trade = trading_robot.create_trade(
	# 	trade_id='long_enter',
	# 	enter_or_exit='enter',
	# 	long_or_short='long',
	# 	order_type='mkt'
	# )
	#
	# # Add an Order Leg
	# new_enter_trade.instrument(
	# 	symbol=trading_symbol,
	# 	quantity=1,
	# 	asset_type='EQUITY'
	# )
	#
	# # Create a new Trade Object for Exiting position
	# new_exit_trade = trading_robot.create_trade(
	# 	trade_id='long_exit',
	# 	enter_or_exit='exit',
	# 	long_or_short='long',
	# 	order_type='mkt'
	# )
	#
	# # Add an Order Leg
	# new_exit_trade.instrument(
	# 	symbol=trading_symbol,
	# 	quantity=1,
	# 	asset_type='EQUITY'
	# )

	# Define a trading dictionary
	# trades_dict = {
	# 	trading_symbol: {
	# 		'buy': {
	# 			'trade_func': trading_robot.trades['long_enter'],
	# 			'trade_id': trading_robot.trades['long_enter'].trade_id
	# 		},
	# 		'sell': {
	# 			'trade_func': trading_robot.trades['long_exit'],
	# 			'trade_id': trading_robot.trades['long_exit'].trade_id
	# 		},
	# 	}
	# }

	# Define the ownership
	# todo Check if I already own the stock when I startup
	ownership_dict = {
		trading_symbol: False
	}

	# Initialize order variable
	order = None

	# signals = indicator_client.check_signals()

	# Execute trade
	# trading_robot.execute_signals(
	# 	signals=signals,
	# 	trades_to_execute=trades_dict
	# )
	#
	# ownership_dict[trading_symbol] = True
	# order: Trade = trades_dict[trading_symbol]['buy']['trade_func']

	#########################################

	while trading_robot.regular_market_open:
		# while True:
		# Grab the latest bar
		latest_bars = trading_robot.get_latest_bar()
		# Add to the stock frame
		trading_robot.portfolio.stock_frame.add_rows(data=latest_bars)

		# Set order legs
		trades_dict = set_trade(trading_robot,
		                        trading_symbol,
		                        indicator_client.price_data_frame['open'],
		                        trading_robot.get_accounts(account_number=ACCOUNT_NUMBER)[0]['available_funds'],
		                        .5)

		# Refresh the indicators
		indicator_client.refresh()

		# Check for the signals
		# signals = indicator_client.check_signals()
		# Define the buy and sell signals
		signals = conf_val.define_signals(
			indicator_client,
			ownership_dict[trading_symbol],
			trading_symbol,
			trading_robot.get_accounts(account_number=ACCOUNT_NUMBER)
		)

		buys = signals['buys'].to_list()
		sells = signals['sells'].to_list()

		print("=" * 50)
		print("Current Signals: ")
		print("-" * 50)
		# print("Symbol: {}".format(list(trades_dict.keys())[0]))
		print("Symbol: {}".format(trading_symbol))
		print("Ownership Status: {}".format(ownership_dict[trading_symbol]))
		print(f"Buy signals: {bcolors.OKGREEN}{buys}{bcolors.ENDC}")
		print(f"Sell Signals: {bcolors.FAIL}{sells}{bcolors.ENDC}")
		print(trading_robot.portfolio.stock_frame.symbol_groups.tail(n=3))
		print("-" * 50)
		print("")

		# Buy or Sell!!!
		if ownership_dict[trading_symbol] is False and buys:

			# Execute trade
			trading_robot.execute_signals(
				signals=signals,
				trades_to_execute=trades_dict
			)

			ownership_dict[trading_symbol] = True
			order: Trade = trades_dict[trading_symbol]['buy']['trade_func']

		elif ownership_dict[trading_symbol] is True and sells:

			# Execute trade
			trading_robot.execute_signals(
				signals=signals,
				trades_to_execute=trades_dict
			)

			ownership_dict[trading_symbol] = False
			order: Trade = trades_dict[trading_symbol]['sell']['trade_func']

		# Grab the last row
		last_row = trading_robot.stock_frame.frame.tail(n=1)

		# Grab the last bar timestamp
		last_bar_timestamp = last_row.index.get_level_values(1)

		# Wait till the next bar
		trading_robot.wait_till_next_bar(last_bar_timestamp=last_bar_timestamp)

	# Close out of trades for the day
	if ownership_dict[trading_symbol] is True:
		signals = trade_utils.sell_out_signal(trading_symbol)
		trades_to_execute = trade_utils.sell_out_trade_to_execute(
			trading_symbol,
			trading_robot
		)
		trading_robot.execute_signals(
			signals=signals,
			trades_to_execute=trades_to_execute
		)
		# Don't need this now but maybe in the future when it
		#  runs on it's own between days
		ownership_dict[trading_symbol] = False
