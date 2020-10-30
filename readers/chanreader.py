import requests
import re
import html.parser
# import json

from .webreader import WebReader


class ChanReader(WebReader):

    # The parameter here is the board ID
    url_string_format = "https://a.4cdn.org/{0}/1.json"
    url_string = ""

    url_boards = 'https://a.4cdn.org/boards.json'

    def __init__(self, board):
        self.url_string = self.url_string_format.format(board)

    def list_boards(self):
        boards = requests.get(self.url_boards).json()['boards']
        print(len(boards))

    # Overrides WebReader.parse()
    def parse(self):
        ret_string = ""
        overall_len = 0
        threads = requests.get(self.url_string).json()['threads']
        for i in range(0, len(threads)):
            if overall_len > self.MAX_LENGTH:
                break
            thread_posts = threads[i]['posts']
            for j in range(0, len(thread_posts)):
                if overall_len > self.MAX_LENGTH:
                    break

                # Replace all quote/HTML references
                if 'com' in thread_posts[j]:
                    post_text_original = html.parser.unescape(thread_posts[j]['com'])
                    post_text = post_text_original.replace("<br>", " ")
                    # re.sub(r"<br>", " ", post_text_original)
                    post_text = re.sub(r">>(\d)+", "", post_text)
                    post_text = re.sub(r"</?(a|span)(\s+[^>]+)>", "", post_text)
                    # Split the text into a list separated by spaces to define "words"
                    words = post_text.split(' ')

                    for word in words:
                        if overall_len > self.MAX_LENGTH:
                            break
                        ret_string += " " + word
                        overall_len += 1

        return re.sub(r"\s+", " ", ret_string).strip()
        # Replace extra whitespace, tab chars, or newline chars

