import operator
import pandas as pd

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators


def define_strat(trading_robot: PyRobot, indicator_client: Indicators):
	"""Set the indicators to reflect the confirmation/validation strategy"""

	indicator_client.ema(period=20, column_name='ema_20')
	indicator_client.ema(period=200, column_name='ema_200')
	indicator_client.rsi(period=14)

	# Calculate the current % gap between the open and current ema_20
	#  This will be used to prevent a buy signal from happening if the open just barely
	#  goes over the ema_20.
	v1 = indicator_client.price_data_frame['open']
	v2 = indicator_client.price_data_frame['ema_20']
	indicator_client.price_data_frame['open_ema_20_percent_diff'] = \
		((v2 - v1) / abs(v1)) * 100

	# indicator_client.set_indicator_signal_compare(
	# 	indicator_1='open',
	# 	indicator_2='ema_20',
	# 	condition_buy=test_stuff,
	# 	condition_sell=test_other
	# )


def test_stuff(ind_1, ind_2):
	return pd.Series(False)


def test_other(ind_1, ind_2):
	return pd.Series(True)


def define_signals(indicator_client: Indicators, owned: bool, trading_symbol: str) -> dict:
	"""Sets buy/sell/hold signals for the conf_val strat"""
	latest_row = indicator_client.price_data_frame.tail(n=1)

	# todo use a better method for accessing these values than [0]
	open_price = latest_row['open'][0]
	ema_20 = latest_row['ema_20'][0]
	ema_200 = latest_row['ema_200'][0]
	rsi = latest_row['rsi'][0]
	percent_diff = latest_row['open_ema_20_percent_diff'][0]

	# print(f"Open: {open_price}, ema_20: {ema_20}, ema_200: {ema_200}, rsi: {rsi}, percent_diff: {percent_diff}")
	# todo determine if I need to have these defaulted to False or just empty
	# todo add the right Series key when marking True for a buy/sell. I think it's the ticker and timestamp
	signals = {
		'buys': pd.Series([]),
		'sells': pd.Series([])
	}

	if owned:
		if ema_200 < ema_20 < open_price and rsi < 80:
			# Hold position
			return signals
		else:
			# Sell
			signals['sells'] = pd.Series([trading_symbol, True])
			return signals
	else:
		if open_price > ema_20 > ema_200 and \
				percent_diff > .5 and rsi < 60:
			# Buy
			signals['buys'] = pd.Series([trading_symbol, True])
			return signals
		# Wait
		# signals['buys'] = pd.Series([trading_symbol, True])
		return signals
