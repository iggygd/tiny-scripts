import keras
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam
import data

#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

#Sequential Keras
model = Sequential([
    Dense(input_size, input_shape=(input_size,)),
    Activation('relu'),
    Dense(input_size),
    Activation('relu'),
    Dense(output_size),
    Activation('sigmoid'),
])

#Compiling and Training
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
dense_1 (Dense)              (None, 784)               615440
_________________________________________________________________
activation_1 (Activation)    (None, 784)               0
_________________________________________________________________
dense_2 (Dense)              (None, 784)               615440
_________________________________________________________________
activation_2 (Activation)    (None, 784)               0
_________________________________________________________________
dense_3 (Dense)              (None, 10)                7850
_________________________________________________________________
activation_3 (Activation)    (None, 10)                0
=================================================================
Total params: 1,238,730
Trainable params: 1,238,730
Non-trainable params: 0
_________________________________________________________________
Train on 60000 samples, validate on 10000 samples
Epoch 1/10
2019-03-22 05:43:05.877071: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
2019-03-22 05:43:06.092771: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
name: GeForce GTX 1060 6GB major: 6 minor: 1 memoryClockRate(GHz): 1.7715
pciBusID: 0000:01:00.0
totalMemory: 6.00GiB freeMemory: 4.97GiB
2019-03-22 05:43:06.103265: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2019-03-22 05:43:07.390979: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-03-22 05:43:07.395439: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2019-03-22 05:43:07.398022: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2019-03-22 05:43:07.401452: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 4722 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1060 6GB, pci bus id: 0000:01:00.0, compute capability: 6.1)
60000/60000 [==============================] - 13s 215us/step - loss: 0.2751 - acc: 0.9138 - val_loss: 0.1818 - val_acc: 0.9412
Epoch 2/10
60000/60000 [==============================] - 10s 174us/step - loss: 0.1367 - acc: 0.9572 - val_loss: 0.1070 - val_acc: 0.9674
Epoch 3/10
60000/60000 [==============================] - 10s 171us/step - loss: 0.1020 - acc: 0.9686 - val_loss: 0.1179 - val_acc: 0.9614
Epoch 4/10
60000/60000 [==============================] - 10s 169us/step - loss: 0.0838 - acc: 0.9742 - val_loss: 0.0995 - val_acc: 0.9683
Epoch 5/10
60000/60000 [==============================] - 11s 175us/step - loss: 0.0730 - acc: 0.9773 - val_loss: 0.0962 - val_acc: 0.9721
Epoch 6/10
60000/60000 [==============================] - 10s 175us/step - loss: 0.0634 - acc: 0.9796 - val_loss: 0.0969 - val_acc: 0.9727
Epoch 7/10
60000/60000 [==============================] - 11s 184us/step - loss: 0.0581 - acc: 0.9826 - val_loss: 0.0957 - val_acc: 0.9746
Epoch 8/10
60000/60000 [==============================] - 12s 193us/step - loss: 0.0517 - acc: 0.9839 - val_loss: 0.1220 - val_acc: 0.9703
Epoch 9/10
60000/60000 [==============================] - 10s 175us/step - loss: 0.0483 - acc: 0.9850 - val_loss: 0.0844 - val_acc: 0.9793
Epoch 10/10
60000/60000 [==============================] - 11s 178us/step - loss: 0.0421 - acc: 0.9866 - val_loss: 0.0902 - val_acc: 0.9802
'''