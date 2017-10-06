from markovmodel import MarkovModel
from re import sub

"""Quick script for demoing the markov model"""

filepath = "./alice.txt"

mkv = MarkovModel(filepath)

print(mkv.generate(15))
