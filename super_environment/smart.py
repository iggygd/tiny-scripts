import keras
from keras.layers import Dense, Input, Flatten
from keras.models import Model
import object

class Smart(NPC):
    def __init__(self, x, y, char):
        super().__init__(x, y, char)
        self.model = None

class Simple(Smart):
    def __init__(self, x, y, char):
        '''
        Simple agents have an input of 5*5 and an output of 9
        '''
        super().__init__(x, y, char)

        inputs = Input(shape=(5,5))
        x = Flatten(inputs)
        x = Dense(9, activation='relu')(x)
        outputs = Dense(9, activation='sigmoid')(x)

        self.model = Model(inputs=inputs, outputs=outputs)


