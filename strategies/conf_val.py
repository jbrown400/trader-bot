import operator
import time

from datetime import datetime
from datetime import timedelta

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators
from configs.config import *


def conf_val(trading_robot: PyRobot, indicator_client: Indicators):
	"""Set the indicators to reflect the confirmation/validation strategy"""

	indicator_client.ema(period=20, column_name='ema_20')
	indicator_client.ema(period=200, column_name='ema_200')

	# Add a Signal Check for price above ema 20
	indicator_client.set_indicator_signal_compare(
		indicator_1='open',
		indicator_2='ema_20',
		condition_buy=operator.ge,
		condition_sell=operator.le
	)

	# Add a signal check to make sure we're in an uptrend
	indicator_client.set_indicator_signal_compare(
		indicator_1='ema_20',
		indicator_2='ema_200',
		condition_buy=operator.ge,
		condition_sell=operator.le
	)
