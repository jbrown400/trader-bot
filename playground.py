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
