import operator
import time

from datetime import datetime
from datetime import timedelta

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators
from configs.config import *


trading_bot = PyRobot(
	client_id=CLIENT_ID,
	redirect_uri=REDIRECT_URI,
	credentials_path=JSON_PATH,
	paper_trading=True
)

trading_robot_portfolio = trading_bot.create_portfolio()

trading_symbol = 'F'

print("Pre market open: ", trading_bot.pre_market_open)
print("Regular market open: ", trading_bot.regular_market_open)
print("Post market open: ", trading_bot.post_market_open)

trading_robot_portfolio.add_position(
	symbol=trading_symbol,
	asset_type='equity',
)

end_date = datetime.today()
# end_date = datetime.fromtimestamp(1600693200000/1000)
start_date = end_date - timedelta(days=20)

# Get historical data
last_20_days = trading_bot.grab_historical_prices(
	start=start_date,
	end=end_date,
	bar_size=1,
	bar_type='minute'
)

# Convert data to a stock frame
stock_frame = trading_bot.create_stock_frame(
	data=[last_20_days['aggregated']]
)

# Add the stock frame to the portfolio
trading_bot.portfolio.stock_frame = stock_frame
trading_bot.portfolio.historical_prices = last_20_days

# Create new indicator client
indicator_client = Indicators(price_data_frame=stock_frame)
indicator_client.ema(period=20, column_name='ema_20')
indicator_client.ema(period=200, column_name='ema_200')

# Add a Signal Check
indicator_client.set_indicator_signal_compare(
	indicator_1='ema_20',
	indicator_2='ema_200',
	condition_buy=operator.ge,
	condition_sell=operator.le
)

# Create a new Trade Object for Entering position
new_enter_trade = trading_bot.create_trade(
	trade_id='long_enter',
	enter_or_exit='enter',
	long_or_short='long',
	order_type='mkt'
)

# Add an Order Leg
new_enter_trade.instrument(
	symbol=trading_symbol,
	quantity=1,
	asset_type='EQUITY'
)

# Create a new Trade Object for Exiting position
new_exit_trade = trading_bot.create_trade(
	trade_id='long_exit',
	enter_or_exit='exit',
	long_or_short='long',
	order_type='mkt'
)

# Add an Order Leg
new_exit_trade.instrument(
	symbol=trading_symbol,
	quantity=1,
	asset_type='EQUITY'
)

# Define a trading dictionary
trades_dict = {
	trading_symbol: {
		'buy': {
			'trade_func': trading_bot.trades['long_enter'],
			'trade_id': trading_bot.trades['long_enter'].trade_id
		},
		'sell': {
			'trade_func': trading_bot.trades['long_exit'],
			'trade_id': trading_bot.trades['long_exit'].trade_id
		},
	}
}

# Define the ownership
ownership_dict = {
	trading_symbol: False
}

# Initialize order variable
order = None

while trading_bot.regular_market_open:
	print("Hello")
	time.sleep(5)
