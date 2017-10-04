from markovmodel import MarkovModel
from re import sub

"""Quick script for demoing the markov model"""

filepath = "./alice.txt"

with open(filepath, 'r') as file:
    lines = file.read().lower()
    print(sub("[^\w]", " ", lines))

mkv = MarkovModel(filepath, 5)

print(mkv.generate(15))
