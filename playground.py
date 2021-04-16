"""
Playground file for code examples from the TF/Scikit book
"""
import tensorflow
from tensorflow import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV
from datetime import datetime

import os
root_logdir = os.path.join(os.curdir, "my_logs")


def main():
	milli = datetime.strptime('2020-09-21 08:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000

	print(milli)

# stock_frame.frame.to_csv('./data/TSLA_data.csv', mode='a', sep=',')
# streaming_client = trading_bot.session.create_streaming_session()
# streaming_client.quality_of_service(qos_level='moderate')
# streaming_client.level_one_quotes(symbols=["CCL"], fields=list(range(0, 15)))
#
# asyncio.run(data_pipeline(streaming_client))

# playground.robot()

# with open('./data/TSLA_data.csv', 'a') as f:
# 	stock_frame.frame.to_csv(f, header=False)
# stock_frame.frame.to_csv('./data/TSLA_data.csv', mode='a', sep=',')

# pprint.pprint(stock_frame)

# pprint.pprint(trading_bot.grab_current_quotes())
