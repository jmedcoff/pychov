# Pychov

Discord bot written in python for automated humorous (and generally useless but still fun) text generation.

## Structure

Given a bank of text accumulated by a web scraper, we would like to design a piece of software that will use the text bank as training to compose new text automatically. Ideally, we would like this to be based on randomized processes sufficiently such that a unique output will be produced almost every time the generating code is run.

The bot will be partitioned into the following components, of tentatively increasing difficulty to implement.

### Server application

This is the "main" component of the bot of sorts, allowing it to be run as a server process in some fashion. It will be important in the long run, but for development purposes, it can probably safely be left for last.

### Web scraper

Software to utilize RESTful gets to compose the text bank. Important questions include how often to scrape, where to scrape, when and if discarding older material is applicable, etc. Most important early-game component. What we really should do here is write a scraper in the abstract, and then subclass from it a specific implemenation on a per-site or per-REST api basis. That way we can easily extend the use of the bot to other sites as well.

A perhaps better idea: write an abstract *reader* class from which an abstract scraper class is derived. From the reader class we can then derive file readers as well, so we are not restricted to web based text. Then we can derive from the scraper class for the websites we want to gather text. Then the server can depend on the reader abstraction and the reader that we actually give it can be anything we want. We should do this. It's much more programmatically prudent.

### Discord bot client

Integration with discord's bot api. Can also wait until later in the development. This should accept some commands with regards to, at the very least, length and source.

### Text generator

Machine learning or Markov chain text generation algo goes here. We need to figure out what to use: markov chain, tensorflow, etc. Other important question os how we decide how long a generated string should be. How do we specify this? Can we specify this on the fly through the discord bot?


## Stages of development

Since the web scraper is so important for early experimentation and figuring out the generator, we will begin with it. Once we have an abstract class defined for the reader, we can begin work on the generator in parallel.

Once these items are finished and conversing nicely, we should begin research on [discord.py](https://github.com/Rapptz/discord.py) for the implementation of the bot.

After the bot has some good progress on it, we can look to start wrapping up the integration by constructing the server application, which will likely amount to a shell script and some additional simple python code. We can also think about giving the bot its own shell commands with the [cmd module.](https://docs.python.org/3/library/cmd.html)

## Further work

It might be interesting from a linguistically analytic point of view to abstract sentence structure from the generated text. We could then statistically analyze the frequency of major vs minor sentences, syntactic structure, etc. This is probably for if we get very bored.

Obviously because of the immateriality of the reader class, we should be able to subclass it and design readers for all sorts of sources: webpages, files, even live feeds.
