import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import np_mnist
import data
import numpy as np

dummy_items = 100
dummy_inputs = np.random.randn(dummy_items,10)
dummy_outputs = np.random.randn(dummy_items,1)

#_, _, train_images, train_labels, _, _, _ = data.mnist.Preprocessed()
#print(train_images.shape)
#print(train_labels.shape)

model = np_mnist.Model(10,1)
model.add(10, 10, np_mnist.Activator.relu, 'L1')
model.add(10, 10, np_mnist.Activator.relu, 'L2')
model.add(10, 1, np_mnist.Activator.sigmoid, 'L3')

print(dummy_inputs.T.shape)
print(dummy_inputs.shape)
x = model.forward(dummy_inputs.T)
print(x.shape)

loss = model.loss(x, dummy_outputs) 
print(loss)