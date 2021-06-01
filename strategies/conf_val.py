import operator
import pandas as pd

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators


def define_strat(trading_robot: PyRobot, indicator_client: Indicators):
	"""Set the indicators to reflect the confirmation/validation strategy"""

	indicator_client.ema(period=20, column_name='ema_20')
	indicator_client.ema(period=200, column_name='ema_200')
	indicator_client.rsi(period=14)


# indicator_client.set_indicator_signal_compare(
# 	indicator_1='open',
# 	indicator_2='ema_20',
# 	condition_buy=test_stuff,
# 	condition_sell=test_other
# )


def test_stuff(ind_1, ind_2):
	return pd.Series({'hi': True})


def test_other(ind_1, ind_2):
	return pd.Series({})


def define_signals(indicator_client: Indicators, owned: bool, trading_symbol: str,
                   bot_account: dict) -> dict:
	"""Sets buy/sell/hold signals for the conf_val strat"""

	# Calculate the current % gap between the open and current ema_20
	#  This will be used to prevent a buy signal from happening if the open just barely
	#  goes over the ema_20.
	v1 = indicator_client.price_data_frame['open']
	v2 = indicator_client.price_data_frame['ema_20']
	v3 = indicator_client.price_data_frame['ema_200']
	indicator_client.price_data_frame['open_ema_20_percent_diff'] = \
		((v1 - v2) / abs(v2)) * 100
	indicator_client.price_data_frame['ema_20_ema_200_percent_diff'] = \
		((v2 - v3) / abs(v3)) * 100

	# todo clean (normalize) latest row

	# todo this is where I would pass the latest row to the ML models

	# Grab the latest row
	latest_row = indicator_client.price_data_frame.tail(n=1)

	# todo use a better method for accessing these values than [0]
	available_funds = bot_account[0]['available_funds']
	open_price = latest_row['open'][0]
	close_price = latest_row['close'][0]
	ema_20 = latest_row['ema_20'][0]
	ema_200 = latest_row['ema_200'][0]
	rsi = latest_row['rsi'][0]
	open_ema_20_percent_diff = latest_row['open_ema_20_percent_diff'][0]
	ema_20_ema_200_percent_diff = latest_row['ema_20_ema_200_percent_diff'][0]

	signals = {
		'buys': pd.Series(),
		'sells': pd.Series()
	}

	if owned:
		if ema_200 < ema_20 < open_price and rsi < 80:
			# Hold position
			return signals
		else:
			# Sell
			signals['sells'] = pd.Series({trading_symbol: True})
			return signals
	else:
		a = close_price > open_price > ema_20 > ema_200
		b = open_ema_20_percent_diff > .5
		c = ema_20_ema_200_percent_diff > .1
		d = rsi < 60

		print("A: ", a)
		print("B: ", b)
		print("C: ", c)
		print("D: ", d)
		# If a wide gap on confirmation, a low RSI, and the price of the
		#  security is 80% of my available funds
		if a and \
				b and \
				c:
			# open_price < (available_funds * .8) and \
			# Buy
			signals['buys'] = pd.Series({trading_symbol: True})
			return signals
		# Wait
		# signals['buys'] = pd.Series([trading_symbol, True])
		return signals
