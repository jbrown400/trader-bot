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

from pyrobot.robot import PyRobot
from pyrobot.robot import Trade
from pyrobot.indicators import Indicators
from configs.config import *
from core.main import Trainer
import playground
from core.actions.get_data import *

# todo Check if orders were filled before trying to sell


if __name__ == '__main__':

	trading_robot = PyRobot(
		client_id=CLIENT_ID,
		redirect_uri=REDIRECT_URI,
		credentials_path=JSON_PATH,
		paper_trading=False
	)

	trading_robot_portfolio = trading_robot.create_portfolio()

	trading_symbol = 'F'

	# print("Pre market open: ", trading_robot.pre_market_open)
	# print("Regular market open: ", trading_robot.regular_market_open)
	# print("Post market open: ", trading_robot.post_market_open)

	trading_robot_portfolio.add_position(
		symbol=trading_symbol,
		quantity=1,
		asset_type='equity',
	)

	end_date = datetime.today()
	# end_date = datetime.fromtimestamp(1600693200000/1000)
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

	# Create new indicator client
	indicator_client = Indicators(price_data_frame=stock_frame)
	indicator_client.ema(period=20, column_name='ema_20')
	indicator_client.ema(period=20, column_name='ema_200')
	# indicator_client.rsi(period=10)

	# Add a Signal Check
	indicator_client.set_indicator_signal_compare(
		indicator_1='ema_20',
		indicator_2='ema_200',
		condition_buy=operator.ge,
		condition_sell=operator.le
	)

	# Create a new Trade Object for Entering position
	new_enter_trade = trading_robot.create_trade(
		trade_id='long_enter',
		enter_or_exit='enter',
		long_or_short='long',
		price=9.00,
		order_type='lmt'
	)

	# Add an Order Leg
	new_enter_trade.instrument(
		symbol=trading_symbol,
		quantity=1,
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
		quantity=1,
		asset_type='EQUITY'
	)

	# Define a trading dictionary
	trades_dict = {
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

	# trades_dict = {
	# 	'MSFT': {
	# 		'trade_func': trading_robot.trades['long_msft'],
	# 		'trade_id': trading_robot.trades['long_msft'].trade_id
	# 	}
	# }

	# Define the ownership
	# todo Check if I already own the stock when I startup
	ownership_dict = {
		trading_symbol: False
	}

	# Initialize order variable
	order = None

	signals = indicator_client.check_signals()

	# Execute trade
	trading_robot.execute_signals(
		signals=signals,
		trades_to_execute=trades_dict
	)

	ownership_dict[trading_symbol] = True
	order: Trade = trades_dict[trading_symbol]['buy']['trade_func']

	#########################################

	# while trading_bot.regular_market_open:
	# while True:
	# 	# Grab the latest bar
	# 	latest_bars = trading_robot.get_latest_bar()
	# 	# Add to the stock frame
	# 	stock_frame.add_rows(data=latest_bars)
	#
	# 	# Refresh the indicators
	# 	indicator_client.refresh()
	#
	# 	print("="*50)
	# 	print("Current Stock Frame: ")
	# 	print("-"*50)
	# 	print(stock_frame.symbol_groups.tail())
	# 	print("-"*50)
	# 	print("")
	#
	# 	# Check for the signals
	# 	signals = indicator_client.check_signals()
	#
	# 	# Define the buy and sell
	# 	buys = signals['buys'].to_list()
	# 	sells = signals['sells'].to_list()
	#
	# 	print("=" * 50)
	# 	print("Current Signals: ")
	# 	print("-" * 50)
	# 	# print("Symbol: {}".format(list(trades_dict.keys())[0]))
	# 	print("Symbol: {}".format(trading_symbol))
	# 	print("Ownership Status: {}".format(ownership_dict[trading_symbol]))
	# 	print("Buy signals: {}".format(buys))
	# 	print("Sell Signals: {}".format(sells))
	# 	print(stock_frame.symbol_groups.tail())
	# 	print("-" * 50)
	# 	print("")
	#
	# 	# Buy or Sell!!!
	# 	if ownership_dict[trading_symbol] is False and buys:
	#
	# 		# Execute trade
	# 		trading_robot.execute_signals(
	# 			signals=signals,
	# 			trades_to_execute=trades_dict
	# 		)
	#
	# 		ownership_dict[trading_symbol] = True
	# 		order: Trade = trades_dict[trading_symbol]['buy']['trade_func']
	#
	# 	elif ownership_dict[trading_symbol] is True and sells:
	#
	# 		# Execute trade
	# 		trading_robot.execute_signals(
	# 			signals=signals,
	# 			trades_to_execute=trades_dict
	# 		)
	#
	# 		ownership_dict[trading_symbol] = False
	# 		order: Trade = trades_dict[trading_symbol]['sell']['trade_func']
	#
	# 	# Grab the last row
	# 	last_row = trading_robot.stock_frame.frame.tail(n=1)
	#
	# 	# Grab the last bar timestamp
	# 	last_bar_timestamp = last_row.index.get_level_values(1)
	#
	# 	# Wait till the next bar
	# 	trading_robot.wait_till_next_bar(last_bar_timestamp=last_bar_timestamp)

	# stock_frame.frame.to_csv('./data/TSLA_data.csv', mode='a', sep=',')

	# streaming_client = trading_bot.session.create_streaming_session()
	# streaming_client.quality_of_service(qos_level='moderate')
	# streaming_client.level_one_quotes(symbols=["CCL"], fields=list(range(0, 15)))
	#
	# asyncio.run(data_pipeline(streaming_client))

	# playground.main()

	# with open('./data/TSLA_data.csv', 'a') as f:
	# 	stock_frame.frame.to_csv(f, header=False)
	# stock_frame.frame.to_csv('./data/TSLA_data.csv', mode='a', sep=',')

	# pprint.pprint(stock_frame)

	# pprint.pprint(trading_bot.grab_current_quotes())
