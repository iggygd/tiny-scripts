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
lr = 0.8
hidden_size = 64 #Smaller than other libraries because CPU is only being used

W1 = np.random.randn(hidden_size, input_size)
b1 = np.zeros((hidden_size, 1))      
W2 = np.random.randn(hidden_size, hidden_size)
b2 = np.zeros((hidden_size, 1))
W3 = np.random.randn(output_size, hidden_size)
b3 = np.zeros((output_size, 1))

model = (W1, b1, W2, b2, W3, b3)
#Train
epochs = 1500
#train_images = (train_images*0.5) + 0.5
#test_images = (test_images*0.5) + 0.5

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
Epoch: 0/1500; train_loss[6.537634093642896]
Epoch: 1/1500; train_loss[4.689940420482009]
Epoch: 2/1500; train_loss[3.948826083142939]
Epoch: 3/1500; train_loss[3.907261725349788]
Epoch: 4/1500; train_loss[3.389550446678466]
Epoch: 5/1500; train_loss[3.034952090847671]
...
...
Epoch: 1494/1500; train_loss[0.3385374465644127]
Epoch: 1495/1500; train_loss[0.3384418437521467]
Epoch: 1496/1500; train_loss[0.33834633077447707]
Epoch: 1497/1500; train_loss[0.3382509074944209]
Epoch: 1498/1500; train_loss[0.3381555737749712]
Epoch: 1499/1500; train_loss[0.33806032947910003]
[[ 935    0   17    8    1   20   18    3    5   11]
 [   0 1101    2    1    2    3    4   18   14    5]
 [   5    4  901   24    9    6   11   26   13    5]
 [   4    4   21  864    2   43    1    4   36   14]
 [   0    0   15    1  875    9   14   14   12   52]
 [  18    2   10   46    1  750   17    2   32   12]
 [   9    7   20    5   14   15  880    0   19    2]
 [   3    2   13   16    7    8    2  922   10   43]
 [   4   14   27   37    8   31    9    4  807   13]
 [   2    1    6    8   63    7    2   35   26  852]]
              precision    recall  f1-score   support

           0       0.95      0.92      0.94      1018
           1       0.97      0.96      0.96      1150
           2       0.87      0.90      0.89      1004
           3       0.86      0.87      0.86       993
           4       0.89      0.88      0.89       992
           5       0.84      0.84      0.84       890
           6       0.92      0.91      0.91       971
           7       0.90      0.90      0.90      1026
           8       0.83      0.85      0.84       954
           9       0.84      0.85      0.85      1002

   micro avg       0.89      0.89      0.89     10000
   macro avg       0.89      0.89      0.89     10000
weighted avg       0.89      0.89      0.89     10000
'''