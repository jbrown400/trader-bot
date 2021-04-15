import csv
import datetime
import time

import requests
from configs.config import FINNHUB_API_KEY


class Finnhub:
	"""
	Class that represents the Finnhub API
	"""

	def get_historical_data(symbol):
		# Times need to be in seconds
		start_date = 1514786400  # Jan 1 2018
		current_date = int(round(time.time()))
		url = 'https://finnhub.io/api/v1/stock/candle?' \
		      f'symbol={symbol}&' \
		      'resolution=1&' \
		      f'from={start_date}&' \
		      f'to={current_date}&' \
		      'format=csv&' \
		      'adjusted=true&' \
		      f'token={FINNHUB_API_KEY}'

		# Make the request and save the content of the response
		response = requests.get(url, {
			'Accept': 'application/json',
			'User-Agent': 'finnhub/python'
		}).content

		# Decode and parse the response into a format that can be handled as a csv
		data = csv.reader(response.decode('utf-8').splitlines())

		# todo Add code to create data files if they are not already created

		# Open the file associated with the ticker symbol or create it if it doesn't exist
		path = f'./data/ticker/{symbol}/{symbol}_historical_data.csv'
		data_file = open(path, 'w+')
		writer = csv.writer(data_file, delimiter=',')

		# Write data entries into csv file for cleaning and training
		for line in data:
			# Add in human readable date and time
			if line[0] == 't':
				line += ['datetime']
			else:
				time_in_milliseconds = int(line[0])
				date_and_time = datetime.datetime.fromtimestamp(time_in_milliseconds)
				line += [f'{date_and_time}']
			# write data to csv
			writer.writerow(line)

		data_file.close()
	pass