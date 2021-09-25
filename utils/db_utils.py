import pandas as pd


def get_drop_command(ticker: str):
	return (
		f"""
		drop table {ticker}
		"""
	)


def get_create_command(ticker: str):
	return (
		f"""
		CREATE TABLE IF NOT EXISTS {ticker} (
						time_stamp TIMESTAMP NOT NULL PRIMARY KEY,
						open NUMERIC NOT NULL,
						close NUMERIC NOT NULL,
						high NUMERIC NOT NULL,
						low NUMERIC NOT NULL,
						volume NUMERIC NOT NULL,
						ema_20 NUMERIC NOT NULL,
						ema_200 NUMERIC NOT NUll,
						macd NUMERIC NOT NULL,
						rsi NUMERIC NOT NULL,
						open_ema_20_percent_diff NUMERIC NOT NULL,
						ema_20_ema_200_percent_diff NUMERIC NOT NULL,
						prev_owned BOOLEAN NOT NULL,
						signal TEXT NOT NULL,
						account_value NUMERIC NOT NULL
					)
		"""
	)


def get_insert_command(ticker: str, time_stamp: str, row: pd.Series):
	return (
		f"""
		INSERT INTO {ticker} (time_stamp, open, close, high, low, volume, ema_20, ema_200, macd, rsi,
											open_ema_20_percent_diff, ema_20_ema_200_percent_diff, prev_owned, signal,
											account_value)
								values ('{time_stamp}',
										{row['open']},
										{row['close']},
										{row['high']},
										{row['low']},
										{row['volume']},
										{row['ema_20']},
										{row['ema_200']},
										{row['macd']},
										{row['rsi']},
										{row['open_ema_20_percent_diff']},
										{row['ema_20_ema_200_percent_diff']},
										'{row['prev_owned']}',
										'{row['signal']}',
										{row['account_value']}) ON CONFLICT (time_stamp) DO UPDATE
										SET signal = EXCLUDED.signal
		"""
	)
