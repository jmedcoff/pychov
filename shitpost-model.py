# The model to be trained by the string fetched by the reader code.

import numpy
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

spm = ShitpostModel("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Turpis egestas sed tempus urna et pharetra pharetra. At tempor commodo ullamcorper a lacus vestibulum. Dui nunc mattis enim ut tellus elementum sagittis vitae et. Faucibus vitae aliquet nec ullamcorper sit amet risus nullam. Tortor vitae purus faucibus ornare suspendisse sed nisi. Eleifend quam adipiscing vitae proin sagittis nisl. Fringilla ut morbi tincidunt augue interdum velit euismod in pellentesque. Sed enim ut sem viverra. In vitae turpis massa sed elementum tempus egestas sed. Id diam maecenas ultricies mi eget mauris pharetra. Condimentum mattis pellentesque id nibh. Rhoncus aenean vel elit scelerisque mauris. Quis risus sed vulputate odio ut enim blandit volutpat. Curabitur vitae nunc sed velit dignissim. Sagittis eu volutpat odio facilisis mauris sit amet massa. Pharetra vel turpis nunc eget lorem dolor sed. Imperdiet massa tincidunt nunc pulvinar. Tempus egestas sed sed risus pretium quam vulputate dignissim. Imperdiet proin fermentum leo vel orci porta non pulvinar. Amet mauris commodo quis imperdiet massa tincidunt nunc pulvinar. Blandit libero volutpat sed cras ornare. Molestie a iaculis at erat. Consectetur lorem donec massa sapien faucibus et molestie ac. Feugiat vivamus at augue eget arcu. In ornare quam viverra orci sagittis eu volutpat odio. Tortor at auctor urna nunc id cursus metus aliquam. Scelerisque in dictum non consectetur a erat nam at lectus. Non diam phasellus vestibulum lorem sed risus ultricies tristique nulla. Sed risus pretium quam vulputate dignissim suspendisse in est ante. Tristique senectus et netus et. Magna ac placerat vestibulum lectus mauris. Metus vulputate eu scelerisque felis imperdiet. Id semper risus in hendrerit. Et odio pellentesque diam volutpat commodo. Sodales neque sodales ut etiam sit amet. Ut sem nulla pharetra diam sit amet nisl suscipit. Placerat orci nulla pellentesque dignissim. Mi tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Risus viverra adipiscing at in tellus integer. Feugiat pretium nibh ipsum consequat nisl vel pretium. Aliquet lectus proin nibh nisl. Orci phasellus egestas tellus rutrum. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Fermentum iaculis eu non diam. Elit at imperdiet dui accumsan sit amet nulla. Suscipit adipiscing bibendum est ultricies. Sit amet aliquam id diam maecenas ultricies mi eget mauris. Adipiscing bibendum est ultricies integer. Nunc faucibus a pellentesque sit amet porttitor eget. Eget mi proin sed libero enim sed faucibus turpis in. Mauris cursus mattis molestie a iaculis at erat pellentesque adipiscing. Morbi tempus iaculis urna id volutpat lacus laoreet. Scelerisque eleifend donec pretium vulputate sapien nec sagittis aliquam. Sapien faucibus et molestie ac feugiat. Nunc lobortis mattis aliquam faucibus purus in massa tempor nec. Mollis aliquam ut porttitor leo a. In arcu cursus euismod quis viverra. Odio pellentesque diam volutpat commodo sed egestas egestas fringilla. Risus nec feugiat in fermentum posuere urna nec. Proin gravida hendrerit lectus a. Aliquam etiam erat velit scelerisque in dictum non consectetur. Consectetur lorem donec massa sapien faucibus. Nulla malesuada pellentesque elit eget. Viverra suspendisse potenti nullam ac tortor vitae purus faucibus ornare. Et tortor at risus viverra adipiscing at. Amet justo donec enim diam vulputate. Vehicula ipsum a arcu cursus vitae. Ultrices tincidunt arcu non sodales. Ut diam quam nulla porttitor. Vitae suscipit tellus mauris a diam maecenas sed. Mi in nulla posuere sollicitudin aliquam ultrices sagittis orci. Ipsum consequat nisl vel pretium lectus. Viverra justo nec ultrices dui sapien eget mi proin sed. Egestas fringilla phasellus faucibus scelerisque eleifend donec. Eu non diam phasellus vestibulum lorem sed risus ultricies. Mattis enim ut tellus elementum sagittis vitae et leo duis. Magna eget est lorem ipsum dolor sit. Sed egestas egestas fringilla phasellus faucibus scelerisque. Ipsum consequat nisl vel pretium lectus. Ullamcorper sit amet risus nullam eget felis eget nunc. Proin sed libero enim sed faucibus. In dictum non consectetur a. Ipsum consequat nisl vel pretium lectus quam id leo in. Senectus et netus et malesuada. Vulputate sapien nec sagittis aliquam. Commodo sed egestas egestas fringilla phasellus faucibus scelerisque. Quisque egestas diam in arcu cursus euismod quis viverra. Egestas integer eget aliquet nibh praesent tristique magna sit amet. Gravida neque convallis a cras. Ornare arcu dui vivamus arcu felis bibendum ut. Cursus risus at ultrices mi tempus. Odio aenean sed adipiscing diam donec adipiscing tristique risus nec. Aliquam etiam erat velit scelerisque. Iaculis at erat pellentesque adipiscing commodo elit at. Feugiat sed lectus vestibulum mattis ullamcorper velit sed ullamcorper. Semper feugiat nibh sed pulvinar proin gravida hendrerit. Vivamus arcu felis bibendum ut. Volutpat blandit aliquam etiam erat velit scelerisque in dictum non. Sem et tortor consequat id porta.")


