import time as time_lib
import pytz
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators
from configs.config import *
from core.main import Trainer
import playground


if __name__ == '__main__':

	# trading_bot = PyRobot(
	# 	client_id=CLIENT_ID,
	# 	redirect_uri=REDIRECT_URI,
	# 	credentials_path=JSON_PATH,
	# 	paper_trading=True
	# )

	playground.main()



	# trading_robot_portfolio = trading_bot.create_portfolio()
	#
	# print("Pre market open: ", trading_bot.pre_market_open)
	# print("Regular market open: ", trading_bot.regular_market_open)
	# print("Post market open: ", trading_bot.post_market_open)
	#
	# end_date = datetime.today()
	# start_date = end_date - timedelta(days=100)
	#
	# trading_robot_portfolio.add_position(
	# 	symbol='MSFT',
	# 	asset_type='equity',
	# )
	#
	# today_data = trading_bot.grab_historical_prices(
	# 	start=start_date,
	# 	end=end_date,
	# 	bar_size=1,
	# 	bar_type='minute'
	# )
	#
	# stock_frame = trading_bot.create_stock_frame(
	# 	data=today_data['aggregated']
	# )
	#
	# stock_frame.frame.to_csv('./data/MSFT_today.csv', sep=',')

	# pprint.pprint(trading_bot.grab_current_quotes())
