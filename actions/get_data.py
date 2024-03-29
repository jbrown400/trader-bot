"""
Contains functions for getting data from remote locations
"""

import asyncio
import pprint


async def data_pipeline(streaming_client):
	await streaming_client.build_pipeline()
	while True:

		data = await streaming_client.start_pipeline()

		pprint.pprint(data, indent=4)
		if 'data' in data:
			data_content = data['data'][0]['content']
			# pprint.pprint(data_content, indent=4)
			pass

		elif 'notify' in data:
			pass


def parse_into_data_frame(response_dict):
	"""
	Takes a quote response dictionary and inserts the data
	  into a pandas data frame

	:return:
	"""


def get_historical_data():
	"""
	Gets the raw data from the TD API, filters it, parses the relevant data,
	  then saves the cleaned data into the corresponding security's data file
	  and send the data to the models as environment properties to be acted upon

	:return:
	"""






def get_yesterday_data():
	"""
	Loops through all security symbol's data files, uses the last entry's timestamp as the starting time and
	  pulls all the missing data for each security and saves it to the data file
	:return:
	"""
	pass
