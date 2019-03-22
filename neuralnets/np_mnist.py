import numpy as np
import data

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

#Preliminaries, defining feed_forward, layers model, and backpropagation. 
#Modified from an earlier project (/nn_private.py)
class Activator():
    @classmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @classmethod
    def relu(self, x):
        return x * (x > 0)

class Model():
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.layers = []
        self.input = np.zeros([self.input_size])
        self.output = np.zeros([self.output_size])

    #Only able to add fully connected layers,
    def add(self, input_size, output_size, activator):
        self.layers.append(Layer(input_size, output_size, activator))

    #Categorical Cross Entropy
    def loss(self, pred, true):

    def forward(self, inputs):
        for i, layer in enumerate(self.layers):
            if i == 0:
                layer.variables = layer.activator(np.dot(layer.weights, inputs) + layer.biases)
                x = layer
            else:
                layer.variables = layer.activator(np.dot(layer.weights, x) + layer.biases)
                x = layer

        return x

class Layer():
    def __init__(self, input_size, output_size activator):
        self.weights = np.random.randn(input_size, output_size)
        self.biases = np.zeros(output_size)
        self.variables = np.random.randn(output_size)
        self.activator = activator