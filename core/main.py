import tensorflow as tf
from tensorflow import keras

class Trainer:

	def start(self):
		fashion_mnist = keras.datasets.fashion_mnist
		print(fashion_mnist.load_data())
