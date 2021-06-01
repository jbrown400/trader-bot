"""
Represents a record in a stock's db table
"""


class RawStockRecord:

	# Note: This is raw data record. Additional information (such as volume
	#  delta will be in a different class

	def __init__(self,
	             _id,
	             _time_stamp,
	             _open,
	             _close,
	             _high,
	             _low,
	             _volume,
	             _52wk_high,
	             _52wk_low,):
		pass


"""
{
  "symbol": "string",
  "description": "string",
  "bidPrice": 0,
  "bidSize": 0,
  "bidId": "string",
  "askPrice": 0,
  "askSize": 0,
  "askId": "string",
  "lastPrice": 0,
  "lastSize": 0,
  "lastId": "string",
  "openPrice": 0,
  "highPrice": 0,
  "lowPrice": 0,
  "closePrice": 0,
  "netChange": 0,
  "totalVolume": 0,
  "quoteTimeInLong": 0,
  "tradeTimeInLong": 0,
  "mark": 0,
  "exchange": "string",
  "exchangeName": "string",
  "marginable": false,
  "shortable": false,
  "volatility": 0,
  "digits": 0,
  "52WkHigh": 0,
  "52WkLow": 0,
  "peRatio": 0,
  "divAmount": 0,
  "divYield": 0,
  "divDate": "string",
  "securityStatus": "string",
  "regularMarketLastPrice": 0,
  "regularMarketLastSize": 0,
  "regularMarketNetChange": 0,
  "regularMarketTradeTimeInLong": 0
}
"""