from configs.config import *
from robot.Robot import Robot


def initialize_robot() -> Robot:
	return Robot(client_id=CLIENT_ID,
	             redirect_uri=REDIRECT_URI,
	             credentials_path=JSON_PATH,
	             trading_account=ACCOUNT_NUMBER,
	             paper_trading=True)
