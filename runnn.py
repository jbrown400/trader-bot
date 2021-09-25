import sys
import psycopg2

from robot.Robot import Robot
from trade import trade

from configs.config import *

if __name__ == '__main__':

	# Set up DB
	db_connection = None
	try:
		db_connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
		cur = db_connection.cursor()

	except psycopg2.DatabaseError as e:
		print(f'Error {e}')
		sys.exit(1)
	finally:
		if db_connection:
			db_connection.close()

	# Define trading ticker
	ticker = 'PLTR'

	# Initialize trading robot
	robot = Robot(client_id=CLIENT_ID,
	              redirect_uri=REDIRECT_URI,
	              credentials_path=JSON_PATH,
	              trading_account=ACCOUNT_NUMBER,
	              ticker=ticker,
	              paper_trading=True)

	trade(robot=robot, db=db_connection, ticker=ticker, trading_type='paper')


