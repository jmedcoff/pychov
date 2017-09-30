import requests
import re
import html.parser
import json
from abc import abstractmethod

MAX_LENGTH = 500  # Max length of words in the string

class WebReader():

    @abstractmethod
    def parse(self):
        """Parse the site and return the string of input text (gets fed into the ML)"""


class ChanReader(WebReader):

    # The parameter here is the board ID
    url_string_format = "https://a.4cdn.org/{0}/1.json"
    url_string = ""

    url_boards = 'https://a.4cdn.org/boards.json'

    def __init__(self):
        self.url_string = self.url_string_format.format(3)

    def list_boards(self):
        boards = requests.get(self.url_boards).json()['boards']
        print(len(boards))

    def parse(self):
        ret_string = ""
        overall_len = 0
        threads = requests.get(self.url_string).json()['threads']
        for i in range(0, len(threads)):
            if overall_len > MAX_LENGTH:
                break
            threadPosts = threads[i]['posts']
            for j in range(0, len(threadPosts)):
                if overall_len > MAX_LENGTH:
                    break

                # Replace all quote/HTML references
                post_text_original = html.parser.unescape(threadPosts[j]['com'])
                post_text = post_text_original.replace("<br>", " ") # re.sub(r"<br>", " ", post_text_original)
                post_text = re.sub(r">>(\d)+", "", post_text)
                post_text = re.sub(r"</?(a|span)(|\s+[^>]+)>", "", post_text)

                # Split the text into a list separated by spaces to define "words"
                words = post_text.split(' ')
                for word in words:
                    if overall_len > MAX_LENGTH:
                        break

                    ret_string += " " + word
                    overall_len += 1

        return re.sub(r"\s+", " ", ret_string).strip()  # Replace extra whitespace, tab chars, or newline chars


x = ChanReader()
print(x.parse())
