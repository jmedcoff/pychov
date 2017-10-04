from abc import abstractmethod, ABC


class WebReader(ABC):

    MAX_LENGTH = 500  # Max length of words in the string

    @abstractmethod
    def parse(self):
        """Parse the site and return the string of input text (gets fed into the model)"""
        pass
