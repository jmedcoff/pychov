import discord
import asyncio
from random import choice
from markovmodel import MarkovModel
from chanreader import ChanReader

file_path = "./textbank.txt"
boards = ["b"]

reader = ChanReader(boards[0])
client = discord.Client()
model = MarkovModel(file_path)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print()

help_msg = "If you would like for me to write a shitpost, just message !post in the desired channel. \n"
help_msg += "To see this help dialog, type !help. For more information, see github.com/jorts1114/pychov."

meme_msg = ["Thank you. I'm doing my best. ;P", "Hmph. I AM the superior shitposter. >:)",
            "Your praise makes me feel validated. I wish I had a more meaningful purpose. :(",
            "Flattery will get you nowhere. My heart belongs to my creator and no one else. <3",
            "You're god damn right. B)", "Who shitposts better: me, or Atnosh? :]",
            "I'm glad I could be of service. ;D", "Do you really mean it? :D"]
@client.event
async def on_message(message):

    # Display a basic help message.
    if message.content.startswith('!help'):
        await client.send_message(message.channel, help_msg)

    # Extra spicy meme for fun.
    if message.content.startswith('!goodbot'):
        await client.send_message(message.channel, choice(meme_msg))

    # Post a randomized shitpost from the markov model.
    elif message.content.startswith('!post'):
        msg = model.generate(20)
        await client.send_message(message.channel, msg)

    # Scrape board of choice and add text to the bank. Format: "!add b"
    elif message.content.startswith('!add'):
        inmsg = message.content.split()
        inboard = inmsg[1].strip()
        newreader = ChanReader(inboard)
        with open(file_path, 'a') as file:
            file.write(newreader.parse())
        boards.append(inboard)

    # Scrape board of choice and clean write text to the bank. Format: "!clean pol"
    elif message.content.startswith('!clean'):
        inmsg = message.content.split()
        inboard = inmsg[1].strip()
        newreader = ChanReader(inboard)
        boards.clear()
        with open(file_path, 'w') as file:
            file.write(newreader.parse())
        boards.append(inboard)






