# The model to be trained by the string fetched by the reader code.

import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


class ShitpostModel:
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




sm = ShitpostModel(text=">Use: CaptureReality and 3dsmax v-ray RT and adv. rendering only. My base server rig (budget 15k to 20k): >Nvidia Quadro P6000 >Some kind of graphics accelerator loaded on Motherboard. >Super-fast storage hooked up on PCI directly on motherboard. What do you think? Should I replace the graphics accelerated P6000 with 3 NVidias 1080Tis? I ll buy a second licence for capturerality. Sorry I meant 4 Nvidias 1080Tis, not 3 hello, i'm working on a very cool project (hardware) and I need a kind of hub for connecting multiple things, I found a very cool model to use, but I don't have the actual 3d model for it, do you have any idea where I can find it ? That's not how they suck. Who's the retard that made that? Sage, to avoid spreading zoological misconceptions. why not pay money for the things you want? Why don't you just model it yourself instead of literally being a useless leech? If it's the pic you posted, that shouldn't take long at all. If you require literally every part of the project to be handed to you, what part are you even doing? Objectively, what makes Houdini better than Maya 2018? My guess is nothing, you are all shills. When I used it 6 months ago it was all just useless VOPS / SOPS / shit without meaning, just a big spaghetti mess. The meme ends now! Who gives a shit about industry standards except wage cucks who like getting treated like shit and fired from their companies for no reason? I know how to use almost all 3d softwares out there and Blender is WAY better than Maya when it comes to poly modeling.I don't care if Blender is free, it's still a very good software for freelancers. >Who gives a shit about industry standards except wage cucks who like getting treated like shit and fired from their companies for no reason? projecting a little too hard, aren't we? Absolutely not, I make more money as a Freelancer than I'd ever make as a wageslave. >says someone with no benefits, no paid vacation, no office parties, no award shows kek lol I know it's been used for more but there was a whole movie made with blender, it was also used in Warcraft and Lights Out. It's not the best program out there but damn man, every program that comes across this board holds it's own weight. It's ignorant and a dumb mindset to think one program is better than others. They ALL have")



