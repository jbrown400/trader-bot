import time as time_lib
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators
from configs.config import *
import tda


if __name__ == '__main__':

	trading_bot = PyRobot(
		client_id=CLIENT_ID,
		redirect_uri=REDIRECT_URI,
		credentials_path=JSON_PATH,
		paper_trading=True
	)
