"""
Playground file for code examples from the TF/Scikit book
"""
import tensorflow
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt

def main():
	# fashion_mnist = keras.datasets.fashion_mnist
	# # fashion mnist data is already broken into train and test sets
	# (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
	# # Create a validation set and scale down all sets from 0-255 to 0-1
	# X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
	# y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
	# X_test = X_test / 255.0
	#
	# # classification labels
	# class_names = ["T-shirt/top", "Trouser", "Pullover", "dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
	#
	# # Build the neural network
	# model = keras.models.Sequential()
	# # This takes the 28x28 array of an image and puts each pixel as a single input for this layer. So freaking cool :D
	# #  we could have also used keras.layers.InputLayer(input_shape=[28,28])
	# model.add(keras.layers.Flatten(input_shape=[28, 28]))
	# model.add(keras.layers.Dense(300, activation="relu"))
	# model.add(keras.layers.Dense(100, activation="relu"))
	# # This acts at the output layer. We chose 10 neurons because there are 10 output classes.
	# # We use softmax b/c the classes are exclusive and we want to get the highest value neuron
	# model.add(keras.layers.Dense(10, activation="softmax"))
	#
	# # View a summary of the model
	# # print(model.summary())
	#
	# # View the weights on a particular layer
	# # print(model.layers[1].get_weights())
	#
	# model.compile(loss="sparse_categorical_crossentropy", optimizer=keras.optimizers.SGD(lr=0.01), metrics=["accuracy"])
	#
	# # Train the model
	# history = model.fit(X_train, y_train, epochs=30, validation_data=(X_valid, y_valid))

	# pd.DataFrame(history.history).to_csv('data.csv', sep='\t')
	df = pd.read_csv('data.csv', sep='\t')
	print(df)

	# Visualize the loss, accuracy, validation loss, and validation accuracy
	# pd.DataFrame(history.history).plot(figsize=(8, 5))

	# fig = plt.figure()
	df.plot(figsize=(8, 5))
	plt.subplot2grid((1, 4), (0, 0), colspan=3)

	# table_subplot = plt.subplot2grid((1, 4), (0, 1))
	table = plt.table(cellText=df)

	plt.grid(True)
	plt.gca().set_ylim(0, 1)  # Set the vertical range to [0-1]
	# Add a data table next to the graph

	plt.show()
