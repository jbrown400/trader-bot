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
from core.actions.get_data import *


if __name__ == '__main__':

	trading_bot = PyRobot(
		client_id=CLIENT_ID,
		redirect_uri=REDIRECT_URI,
		credentials_path=JSON_PATH,
		paper_trading=True
	)
	streaming_client = trading_bot.session.create_streaming_session()
	streaming_client.quality_of_service(qos_level='moderate')
	streaming_client.level_one_quotes(symbols=["CCL"], fields=list(range(0, 15)))

	asyncio.run(data_pipeline(streaming_client))

	# streaming_client = trading_bot.session.create_streaming_session()

	# streaming_client.write_behavior(
	# 	write='csv',
	# 	file_path="./data/CCL_data.csv",
	# 	append_mode=True
	# )
	# streaming_client.quality_of_service(qos_level='express')
	# streaming_client.level_one_quotes(symbols=["CCL"], fields=list(range(0, 15)))
	# streaming_client.level_one_quotes(symbols=["CCL"], fields=["1"])
	# streaming_client.stream()
	# streaming_client.start_pipeline()

	# playground.main()


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
	# 	symbol='CCL',
	# 	asset_type='equity',
	# )

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

	# stock_frame.frame.to_csv('./data/MSFT_today.csv', sep=',')

	# pprint.pprint(trading_bot.grab_current_quotes())
