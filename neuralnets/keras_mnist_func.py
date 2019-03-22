import keras
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import Adam
import data

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

#Functional Keras
inputs = Input(shape=(input_size,))
x = Dense(input_size, activation='relu')(inputs)
x = Dense(input_size, activation='relu')(x)
outputs = Dense(output_size, activation='sigmoid')(x)

#Compiling and Training
model = Model(inputs=inputs, outputs=outputs)
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])
model.summary()
model.fit(train_images, train_labels, epochs=10, verbose=1, batch_size=32, validation_data=(test_images, test_labels))

##Output_________________________________________________________
'''
Using TensorFlow backend.
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         (None, 784)               0
_________________________________________________________________
dense_1 (Dense)              (None, 784)               615440
_________________________________________________________________
dense_2 (Dense)              (None, 784)               615440
_________________________________________________________________
dense_3 (Dense)              (None, 10)                7850
=================================================================
Total params: 1,238,730
Trainable params: 1,238,730
Non-trainable params: 0
_________________________________________________________________
Train on 60000 samples, validate on 10000 samples
Epoch 1/10
2019-03-22 05:32:36.183801: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
2019-03-22 05:32:36.385518: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
name: GeForce GTX 1060 6GB major: 6 minor: 1 memoryClockRate(GHz): 1.7715
pciBusID: 0000:01:00.0
totalMemory: 6.00GiB freeMemory: 4.97GiB
2019-03-22 05:32:36.413752: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2019-03-22 05:32:37.611052: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-03-22 05:32:37.616352: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2019-03-22 05:32:37.619395: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2019-03-22 05:32:37.642357: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 4722 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1060 6GB, pci bus id: 0000:01:00.0, compute capability: 6.1)
60000/60000 [==============================] - 12s 203us/step - loss: 0.2709 - acc: 0.9155 - val_loss: 0.1396 - val_acc: 0.9547
Epoch 2/10
60000/60000 [==============================] - 10s 175us/step - loss: 0.1368 - acc: 0.9581 - val_loss: 0.1303 - val_acc: 0.9586
Epoch 3/10
60000/60000 [==============================] - 10s 171us/step - loss: 0.1045 - acc: 0.9686 - val_loss: 0.0988 - val_acc: 0.9692
Epoch 4/10
60000/60000 [==============================] - 10s 160us/step - loss: 0.0849 - acc: 0.9738 - val_loss: 0.1145 - val_acc: 0.9649
Epoch 5/10
60000/60000 [==============================] - 10s 162us/step - loss: 0.0707 - acc: 0.9780 - val_loss: 0.0972 - val_acc: 0.9710
Epoch 6/10
60000/60000 [==============================] - 9s 158us/step - loss: 0.0631 - acc: 0.9800 - val_loss: 0.1145 - val_acc: 0.9683
Epoch 7/10
60000/60000 [==============================] - 10s 161us/step - loss: 0.0556 - acc: 0.9827 - val_loss: 0.0895 - val_acc: 0.9762
Epoch 8/10
60000/60000 [==============================] - 9s 155us/step - loss: 0.0525 - acc: 0.9834 - val_loss: 0.0907 - val_acc: 0.9768
Epoch 9/10
60000/60000 [==============================] - 10s 159us/step - loss: 0.0468 - acc: 0.9850 - val_loss: 0.0861 - val_acc: 0.9770
Epoch 10/10
60000/60000 [==============================] - 9s 155us/step - loss: 0.0432 - acc: 0.9870 - val_loss: 0.0961 - val_acc: 0.9773
'''