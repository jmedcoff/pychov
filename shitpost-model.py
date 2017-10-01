# The model to be trained by the string fetched by the reader code.

import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


class ShitpostModel:
    def __init__(self, saved_model=None, text=None):
        self.int_to_char = dict((i, c) for i, c in enumerate(self.chars))
        if saved_model is None:
            self.first_run(text)
        else:
            self.load_model(saved_model)

    def load_model(self, saved_model):
        self.model = Sequential()
        self.model.load_weights(saved_model)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

    def first_run(self, text):
        self.chars = sorted(list(set(text)))
        self.char_to_int = dict((c, i) for i, c in enumerate(self.chars))

        self.nchars = len(text)
        self.nvocab = len(self.chars)

        self.slength = 100
        self.datax = []
        self.datay = []

        for i in range(0, self.nchars - self.slength, 1):
            seq_in = text[i:i + self.slength]
            seq_out = text[i + self.slength]
            self.datax.append([ord(char) for char in seq_in])
            self.datay.append([ord(seq_out)])

        self.npatterns = len(self.datax)

        self.X = numpy.reshape(self.datax, (self.npatterns, self.slength, 1))
        numpy.true_divide(self.X, float(self.nvocab), casting='unsafe')
        self.Y = np_utils.to_categorical(self.datay)

        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(self.X.shape[1], self.X.shape[2])))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(self.Y.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

        self.filepath = "weights{epoch:02d}{loss:.4f}"
        self.checkpoint = ModelCheckpoint(self.filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        self.callbacklist = [self.checkpoint]

        self.model.fit(self.X, self.Y, epochs=20, batch_size=128, callbacks=self.callbacklist)
