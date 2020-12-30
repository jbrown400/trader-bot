import operator

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators


def golden_cross(trading_robot: PyRobot, indicator_client: Indicators):
	"""Set the indicators to reflect the golden cross strategy"""

	indicator_client.ema(period=20, column_name='ema_20')
	indicator_client.ema(period=200, column_name='ema_200')

	# Add a Signal Check
	indicator_client.set_indicator_signal_compare(
		indicator_1='ema_20',
		indicator_2='ema_200',
		condition_buy=operator.ge,
		condition_sell=operator.le
	)
