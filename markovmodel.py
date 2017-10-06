from re import sub
from random import randint, choice


class MarkovModel:
    """This is the "model" based off of markov processes instead of machine learning."""

    def __init__(self, file_path, length=4):
        self.length = None
        self.words = None
        self.num_words = None
        self.database = None
        self.load(file_path, length)

    def load(self, file_path, length=4):
        if file_path is None:
            Exception("Cannot initialize without an input file.")

        self.length = length
        with open(file_path, 'r') as file:
            lines = file.read().lower()
            self.words = sub("[^\w]", " ", lines).split()
        self.num_words = len(self.words)
        self.database = {}
        self.__build_database()


    def __build_tuples(self):
        """Build the tuples from the word list for the database"""

        if self.num_words < self.length:
            Exception("Input file size too small.")

        # we need to end with one complete tuple of length "length", which must start
        # at num_words + 1 - length
        for i in range(self.num_words - (self.length - 1)):
            # generators here because we can hold off on processing until we build the database
            yield tuple(self.words[i+j] for j in range(self.length))

    def __build_database(self):
        """Build the database itself."""
        for tup in self.__build_tuples():
            key = tup[0:self.length-1]
            if key in self.database:
                self.database[key].append(tup[-1])
            else:
                self.database[key] = [tup[-1]]
            # What we do here is make the database values lists, to account for strings
            # with same first words. i.e. "the red apple" and "the red truck" =>
            # database[("the", "red")] = ["apple", "truck"]

    def generate(self, size):
        """Generate a string of length "size" from the database."""
        seed = randint(0, self.num_words-self.length)
        w = [x for x in self.words[seed:seed+self.length]]
        out = []
        for i in range(size):
            key = tuple(w)
            if key in self.database:
                next_word = choice(self.database[key])
            else:
                next_word = choice(self.words)
            out.append(w[0])
            del w[0]
            w.append(next_word)
            # Here we consider two words in our string, and use random choice
            # to determine the next word. Add it to the output list, and trim
            # the first word from w. Repeat. If we run into the case where we
            # are looking at the last n words in our string, we just pick a
            # new random word to pick up from. The grammatical impact should
            # be minimal in the grand scheme of things.
        return " ".join(out)
