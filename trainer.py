
class Trainer:

    def __init__(self, text):
        if len(text) > 200:
            first_run(self, text)
        else:
            Exception("Input size is too small.")


