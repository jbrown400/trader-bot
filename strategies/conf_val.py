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


# def criteria_met() -> bool:
# 	"""Returns whether or not a buy condition is met for the conf_val strat"""
# 	if True:
# 		return True
# 	else:
# 		return False
