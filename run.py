from td.client import TDClient
from config.config import *


if __name__ == '__main__':

	TDSession = TDClient(client_id=CLIENT_ID,
	                     redirect_uri=REDIRECT_URI,
	                     credentials_path=JSON_PATH)
	TDSession.login()

	price_history = TDSession.get_price_history(symbol='CCL',
	                                            period_type='year',
	                                            period=2,
	                                            frequency='1',
	                                            frequency_type='daily')

	print(price_history)
