from datetime import datetime
from datetime import timedelta

import pandas as pd
from pyrobot.robot import PyRobot


def sell_out_signal(trading_symbol: str):
	return {
		'buys': pd.Series(),
		'sells': pd.Series({trading_symbol: True})
	}


def sell_out_trade_to_execute(trading_symbol: str, trading_robot: PyRobot):
	# Set the cancel time to 1 day out
	gtc_date = datetime.now() - timedelta(days=1)
	# Create a new Trade Object for Exiting position
	new_exit_trade = trading_robot.create_trade(
		trade_id='sell_out_exit',
		enter_or_exit='exit',
		long_or_short='long',
		order_type='mkt'
	)
	# Make the trade good till cancel
	new_exit_trade.good_till_cancel(gtc_date)

	# todo set the quantity to be the currently held quantity
	# Add an Order Leg
	new_exit_trade.instrument(
		symbol=trading_symbol,
		quantity=1,
		asset_type='EQUITY'
	)

	return {
		trading_symbol: {
			'buy': {},
			'sell': {
				'trade_func': trading_robot.trades['sell_out_exit'],
				'trade_id': trading_robot.trades['sell_out_exit'].trade_id
			},
		}
	}
