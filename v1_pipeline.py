"""
Defines the pipeline for version 1
"""
from models.enums.Duration import Duration
from utils.setup_utils import initialize_robot


def run_v1():
	# Initialize robot
	robot = initialize_robot()
	robot.portfolio.add_position(symbol='PLTR', quantity=1, asset_type='equity')

	# Get and process data
	robot.get_and_process_data(tickers=robot.tickers)

	# Paper trade on data for that day to see how much money was made
	robot.simulate_trading(Duration.TODAY)
