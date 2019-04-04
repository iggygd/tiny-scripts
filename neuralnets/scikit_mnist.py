import data
import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

#Model
hidden_size = 64 #Smaller than other libraries because CPU is only being used
model = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(hidden_size,), verbose=True, max_iter=100)

#Train
model.fit(train_images, train_labels)

#Test
X = model.predict(test_images)
pred = np.argmax(X.T, axis=0)
true = np.argmax(test_labels.T, axis=0)
print(confusion_matrix(pred, true))
print(classification_report(pred, true))

##Output
'''
Iteration 1, loss = 1.08156244
Iteration 2, loss = 0.61971766
Iteration 3, loss = 0.50314510
Iteration 4, loss = 0.43334879
Iteration 5, loss = 0.38449428
...
...
Iteration 95, loss = 0.05745831
Iteration 96, loss = 0.05796201
Iteration 97, loss = 0.05551811
Iteration 98, loss = 0.05593970
Iteration 99, loss = 0.05343222
Iteration 100, loss = 0.05460321
D:\Workspace\2019\tiny_scripts\env\lib\site-packages\sklearn\neural_network\multilayer_perceptron.py:562: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (100) reached and the optimization hasn't converged yet.
  % self.max_iter, ConvergenceWarning)
[[ 976    4   43   21   21   21   21   17   62   38]
 [   0 1128   11    2    2    4    6    7    1    6]
 [   0    1  969    6    1    0    2    9    2    1]
 [   1    2    1  972    1   20    0    4    8    4]
 [   1    0    0    0  948    1   10    2    9   11]
 [   0    0    0    2    0  839    8    0    8    4]
 [   0    0    1    0    4    4  910    2    1    1]
 [   0    0    6    5    1    1    1  987    8   24]
 [   0    0    1    1    0    2    0    0  874    2]
 [   2    0    0    1    4    0    0    0    1  918]]
              precision    recall  f1-score   support

           0       1.00      0.80      0.89      1224
           1       0.99      0.97      0.98      1167
           2       0.94      0.98      0.96       991
           3       0.96      0.96      0.96      1013
           4       0.97      0.97      0.97       982
           5       0.94      0.97      0.96       861
           6       0.95      0.99      0.97       923
           7       0.96      0.96      0.96      1033
           8       0.90      0.99      0.94       880
           9       0.91      0.99      0.95       926

   micro avg       0.95      0.95      0.95     10000
   macro avg       0.95      0.96      0.95     10000
weighted avg       0.95      0.95      0.95     10000
'''