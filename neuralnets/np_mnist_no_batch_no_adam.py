from sklearn.metrics import classification_report, confusion_matrix

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

#Bug with division by zero or matrix multiply error, can't be bothered to debug right now.
def ce_loss(pred, true):
    N = pred.shape[1]
    #print(np.multiply(np.log(true), pred), '001')
    #print(np.multiply(np.log(1 - true), (1 - pred)), '002')
    #inner = np.multiply(np.log(true), pred) + np.multiply(np.log(1 - true), (1 - pred))
    inner = np.multiply(true, np.log(pred))
    loss = -(1/N) * np.sum(inner)

    return loss

def forward(inputs, W1, b1, W2, b2, W3, b3):
    Z1 = np.matmul(W1, inputs) + b1
    A1 = sigmoid(Z1)

    Z2 = np.matmul(W2, A1) + b2
    A2 = sigmoid(Z2)

    Z3 = np.matmul(W3, A2) + b3
    A3 = np.exp(Z3) / np.sum(np.exp(Z3), axis=0)
    #A3 = sigmoid(Z3)
    return (Z1, A1, Z2, A2, Z3, A3)

def backprop(inputs, outputs, Z1, A1, Z2, A2, Z3, A3, W1, b1, W2, b2, W3, b3):
    N = outputs.shape[1]
    factor = 1/N

    dZ3 = A3 - outputs
    #Bug here, shapes are (60000,10), (60000,784); !!Fixed
    #should they be (784,60000)*(60000,10) -> (784,10) or (10,60000)*(60000,784) -> (10,784) 
    #(10,784) looks like the right shape, but try both.
    dW3 = factor * np.matmul(dZ3, A2.T)
    db3 = factor * np.sum(dZ3, axis=1, keepdims=True)

    dA2 = np.matmul(W3.T, dZ3)
    dZ2 = dA2 * sigmoid_prime(Z2)
    dW2 = factor * np.matmul(dZ2, A1.T)
    db2 = factor * np.sum(dZ2, axis=1, keepdims=True)

    dA1 = np.matmul(W2.T, dZ2)
    dZ1 = dA1 * sigmoid_prime(Z1)
    dW1 = factor * np.matmul(dZ1, inputs.T)
    db1 = factor * np.sum(dZ1, axis=1, keepdims=True)

    W3 = W3 - (lr * dW3)
    b3 = b3 - (lr * db3)
    W2 = W2 - (lr * dW2)
    b2 = b2 - (lr * db2)
    W1 = W1 - (lr * dW1)
    b1 = b1 - (lr * db1)

    return (W1, b1, W2, b2, W3, b3)

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()


#Model
lr = 0.7
hidden_size = 64 #Smaller than other libraries because CPU is only being used

W1 = np.random.randn(hidden_size, input_size)
b1 = np.zeros((hidden_size, 1))      
W2 = np.random.randn(hidden_size, hidden_size)
b2 = np.zeros((hidden_size, 1))
W3 = np.random.randn(output_size, hidden_size)
b3 = np.zeros((output_size, 1))

model = (W1, b1, W2, b2, W3, b3)
#Train
epochs = 1000
train_images = (train_images*0.5) + 0.5
test_images = (test_images*0.5) + 0.5

for epoch in range(epochs):
    X = forward(train_images.T, *model)
    loss = ce_loss(X[-1], train_labels.T)
    model = backprop(train_images.T, train_labels.T, *X, *model)
    print(f'Epoch: {epoch}/{epochs}; train_loss[{loss}]')

#Test
X = forward(test_images.T, *model)
pred = np.argmax(X[-1], axis=0)
true = np.argmax(test_labels.T, axis=0)
print(confusion_matrix(pred, true))
print(classification_report(pred, true))

##Output
'''
Epoch: 0/1000; train_loss[8.493202661674912]
Epoch: 1/1000; train_loss[5.473629628032126]
Epoch: 2/1000; train_loss[4.28523171698634]
Epoch: 3/1000; train_loss[3.2610651894420837]
Epoch: 4/1000; train_loss[2.7969275465473316]
Epoch: 5/1000; train_loss[2.5461041629669574]
...
...
Epoch: 995/1000; train_loss[0.3462058771135897]
Epoch: 996/1000; train_loss[0.34606155296457436]
Epoch: 997/1000; train_loss[0.34591742162417966]
Epoch: 998/1000; train_loss[0.34577348264248836]
Epoch: 999/1000; train_loss[0.3456297355710629]
[[ 936    0   19    7    4   17   20    2    7   13]
 [   0 1105    9    3    4    5    4   11    4    9]
 [   7    4  908   25    5   10   10   24   17    7]
 [   3    5   18  866    1   38    2    6   37   13]
 [   0    0   16    1  872   11   18   19   13   54]
 [  11    5    1   46    2  754   11    5   34   10]
 [   7    2   13    3   14   18  883    0    9    3]
 [   7    2   14   13    7    9    0  920   16   35]
 [   6   12   30   30    8   24    9    7  814   10]
 [   3    0    4   16   65    6    1   34   23  855]]
              precision    recall  f1-score   support

           0       0.96      0.91      0.93      1025
           1       0.97      0.96      0.97      1154
           2       0.88      0.89      0.89      1017
           3       0.86      0.88      0.87       989
           4       0.89      0.87      0.88      1004
           5       0.85      0.86      0.85       879
           6       0.92      0.93      0.92       952
           7       0.89      0.90      0.90      1023
           8       0.84      0.86      0.85       950
           9       0.85      0.85      0.85      1007

   micro avg       0.89      0.89      0.89     10000
   macro avg       0.89      0.89      0.89     10000
weighted avg       0.89      0.89      0.89     10000
'''