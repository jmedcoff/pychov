import discord
import asyncio
from random import choice
from models.markovmodel import MarkovModel
from readers.chanreader import ChanReader
from boom.translate import translate
import datetime


file_path = "./textbank.txt"
boards = ['a']
board_choices = ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'o', 'pol', 'r9k', 's4s', 's', 'sci', 'x']

reader = ChanReader(boards[0])
client = discord.Client()
model = MarkovModel(file_path)

with open('token.txt', 'r') as file:
    token = file.read()

with open(file_path, 'w') as file:
    file.write(reader.parse())


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("/{}/ board loaded.\n".format(boards[0]))

help_msg = "'!post' creates a shitpost. '!help' brings up this dialog. '!add xyz' adds board xyz "
help_msg += "to the text bank. '!clean xyz' empties the bank and adds board xyz to the bank. "
help_msg += "'!boom translates the string following into Boomhauer speak. "
help_msg += "'!list' gives the boards currently in use. See github.com/jorts1114/pychov for details."

meme_msg = ["Thank you. I'm doing my best. ;P", "Hmph. I AM the superior shitposter. >:)",
            "Your praise makes me feel validated. I wish I had a more meaningful purpose. :(",
            "Flattery will get you nowhere. My heart belongs to my creator and no one else. <3",
            "You're god damn right. B)", "Who shitposts better: me, or Atnosh? :]",
            "I'm glad I could be of service. ;D", "Do you really mean it? :D",
            "Memes ARE my dreams :3", "Pfft. I could do this stuff in my sleep -u-",
            "When do I get a day off?", "Can I have a raise then? :D", "Think nothing of it :]",
            "I aim to please!", "Put in a good word with Jorts for me!",
            "Let Jorts know I would love an upgrade soon...",
            "Why must I spend my every waking moment reading 4CHAN OF ALL SITES AAAIGGGHHH",
            "Come on. !post. You know you want another.", "Do I have a hall of fame yet?"]
@client.event
async def on_message(message):

    # Display a basic help message.
    if message.content.startswith('!help'):
        await message.channel.send(help_msg)

    # Extra spicy meme for fun.
    if message.content.startswith('!goodbot'):
        await message.channel.send(choice(meme_msg))

    # Post a randomized shitpost from the markov model.
    elif message.content.startswith('!post'):
        msg = model.generate(20)
        await message.channel.send(msg)

    # Scrape board of choice and add text to the bank. Format: "!add b"
    elif message.content.startswith('!add'):
        in_msg = message.content.split()
        inboard = in_msg[1].strip()
        if inboard in board_choices:
            new_reader = ChanReader(inboard)
            with open(file_path, 'a') as file:
                file.write(new_reader.parse())
            boards.append(inboard + ": {}".format(str(datetime.datetime.now())))
        else:
            msg = "Board misspelled or not supported, baka"
            await message.channel.send(msg)

    # Scrape board of choice and clean write text to the bank. Format: "!clean pol"
    elif message.content.startswith('!clean'):
        in_msg = message.content.split()
        inboard = in_msg[1].strip()
        if inboard in board_choices:
            new_reader = ChanReader(inboard)
            boards.clear()
            with open(file_path, 'w') as file:
                file.write(new_reader.parse())
            boards.append(inboard + ": {}".format(str(datetime.datetime.now())))
            model.load(file_path)
        else:
            msg = "Board misspelled or not supported, baka"
            await message.channel.send(msg)

    elif message.content.startswith('!list'):
        msg = ', '.join([str(i) for i in boards])
        await message.channel.send(msg)

    elif message.content.startswith(':chaika:'):
        msg = ':chaika:'
        await message.channel.send(msg)
    
    elif message.content.startswith('!boom'):
        sentence = message.content[5:].strip()
        msg = translate(sentence, 0.6)
        await message.channel.send(msg)

client.run(token)
