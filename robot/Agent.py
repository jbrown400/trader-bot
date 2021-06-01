

class Agent:

	def __init__(self):
		self.model = None
		self.performance = None
		self.last_update_time_stamp = None
		self.id = None
		self.training_methods = ['adversarial', 'k-means', ]

	@property
	def performance(self):
		"""
		Calculate and return current performance metrics...not really sure what that metric will be tho...
		:return: Performance metric
		"""
		return "performance"

	@performance.setter
	def performance(self, value):
		self._performance = value