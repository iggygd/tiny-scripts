import numpy as np
import data

#Preliminaries
#Modified from an earlier project (/nn_private.py)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))

def relu(x):
    return x * (x > 0)

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

def ce_loss(pred, true):
    N = len(pred)
    inner = np.multiply(np.log(true), pred) + np.multiply(np.log(1 - true), (1 - pred))
    loss = -(1/N) * np.sum(inner)

    return loss

#Model
lr = 0.9
W1 = np.random.randn(input_size, input_size)
b1 = np.zeros((1, input_size))      
W2 = np.random.randn(input_size, input_size)
b2 = np.zeros((1, input_size))
W3 = np.random.randn(input_size, output_size)
b3 = np.zeros((1, output_size))

def forward(inputs):
    Z1 = np.dot(inputs, W1) + b1
    A1 = relu(Z1)

    Z2 = np.dot(Z1, W2) + b2
    A2 = relu(Z2)

    Z3 = np.dot(Z2, W3) + b3
    A3 = sigmoid(Z3)

    return (Z1, A1, Z2, A2, Z3, A3)

def backprop(inputs, outputs, Z1, A1, Z2, A2, Z3, A3):
    N = len(outputs)
    factor = 1/N

    dZ3 = A3 - outputs
    dW3 = factor * np.matmul(dZ3, inputs.T)
    db3 = factor * np.sum(dZ3, axis=1, keepdims=True)

    dZ2 = np.dot(dA3, W3.T)
    dA2 = np.dot(dZ2, sigmoid_prime(A2))
    dW2 = factor * np.matmul(dZ2, X.T)
    db2 = factor * np.sum(dZ2, axis=1, keepdims=True)

    dZ1 = np.dot(dA2, W2.T)
    dA1 = np.dot(dZ1, sigmoid_prime(A1))
    dW1 = factor * np.matmul(dZ1, X.T)
    db1 = factor * np.sum(dZ1, axis=1, keepdims=True)

    W3 = W3 - lr * dW3
    b3 = b3 - lr * db3
    W2 = W2 - lr * dW2
    b2 = b2 - lr * db2
    W1 = W1 - lr * dW1
    b1 = b1 - lr * db1

#Train
epochs = 10
for epoch in range(epochs):
    X = forward(train_images)
    loss = ce_loss(X[-1], train_labels)
    backprop(train_images, train_labels, *X)
    print(f'Epoch: {epoch}/{epochs}; train_loss[{loss}]')