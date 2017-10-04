# The model to be trained by the string fetched by the reader code.

import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


class KerasModel:
    """This is the machine learning model using keras over theano"""

    def __init__(self, text):
        self.chars = sorted(list(set(text)))
        self.char_to_int = dict((c, i) for i, c in enumerate(self.chars))

        self.nchars = len(text)
        self.nvocab = len(self.chars)

        self.slength = 20
        self.datax = []
        self.datay = []

        for i in range(0, self.nchars - self.slength, 1):
            seq_in = text[i:i + self.slength]
            seq_out = text[i + self.slength]
            self.datax.append([self.char_to_int[char] for char in seq_in])
            self.datay.append([self.char_to_int[seq_out]])

        self.npatterns = len(self.datax)

        self.X = numpy.reshape(self.datax, (self.npatterns, self.slength, 1))
        numpy.true_divide(self.X, float(self.nvocab), casting='unsafe')
        self.Y = np_utils.to_categorical(self.datay)

        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(self.X.shape[1], self.X.shape[2]), return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256))
        self.model.add(Dense(self.Y.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

        self.filepath = "weights{epoch:02d}{loss:.4f}"
        self.checkpoint = ModelCheckpoint(self.filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        self.callbacklist = [self.checkpoint]

        self.model.fit(self.X, self.Y, epochs=1, batch_size=128, callbacks=self.callbacklist)

        int_to_char = dict((i,c) for i, c in enumerate(self.chars))

        self.start = numpy.random.randint(0, len(self.datax) - 1)
        self.pattern = self.datax[self.start]
        print("Seed: ", "".join([int_to_char[value] for value in self.pattern]))

        output_size = 1000
        for i in range(output_size):
            x = numpy.reshape(self.pattern, (1, len(self.pattern), 1))
            numpy.true_divide(x, float(self.nvocab), casting='unsafe')
            self.prediction = self.model.predict(x, verbose=0)
            index = numpy.argmax(self.prediction)
            self.result = int_to_char[index]
            self.seq_in = [int_to_char[value] for value in self.pattern]
            sys.stdout.write(self.result)
            self.pattern.append(index)
            self.pattern = self.pattern[1:len(self.pattern)]