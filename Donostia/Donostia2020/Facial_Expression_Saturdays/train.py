
import argparse
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense
from tensorflow.keras.layers import Embedding, Dropout
from keras.callbacks import EarlyStopping
import pandas as pd

if __name__ == '__main__':

 
    es = EarlyStopping(monitor='val_loss', patience = 10, mode = 'min', restore_best_weights=True)
    model = Sequential()
    input_shape = (48,48,1)
    model.add(Conv2D(64, (5, 5), input_shape=input_shape,activation='relu', padding='same'))
    model.add(Conv2D(64, (5, 5), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (5, 5),activation='relu',padding='same'))
    model.add(Conv2D(128, (5, 5),activation='relu',padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(256, (3, 3),activation='relu',padding='same'))
    model.add(Conv2D(256, (3, 3),activation='relu',padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(7))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],optimizer='adam')
    model.summary()

    model.fit(x=features, 
            y=labels,
            epochs=10, 
            steps_per_epoch = len(features)/64,
            verbose=1, 
            callbacks = [es],
            validation_data=(test_features,labels_test),  
            validation_steps = len(features)/64)

     tf.saved_model.simple_save(
     tf.keras.backend.get_session(),
     os.path.join(model_dir, '1'),
     inputs={'inputs': model.input},
     outputs={t.name: t for t in model.outputs})
    
