# Pychov

Discord bot written in python for automated shitposting.

## Structure

Given a bank of text accumulated by a web scraper, we would like to design a piece of software that will use the text bank as training to compose new text automatically. Ideally, we would like this to be based on randomized processes sufficiently such that a unique output will be produced almost every time the generating code is run.

The bot will be partitioned into the following components, of tentatively increasing difficulty to implement.

### Server application

This is the "main" component of the bot of sorts, allowing it to be run as a server process in some fashion. It will be important in the long run, but for development purposes, it can probably safely be left for last.

### Web scraper

Software to utilize RESTful gets to compose the text bank. Important questions include how often to scrape, where to scrape, when and if discarding older material is applicable, etc. Most important early-game component. What we really should do here is write a scraper in the abstract, and then subclass from it a specific implemenation on a per-site or per-REST api basis. That way we can easily extend the use of the bot to other sites as well.

### Discord bot client

Integration with discord's bot api. Can also wait until later in the development.

### Text generator

Machine learning or Markov chain text generation algo goes here. We need to figure out what to use: markov chain, tensorflow, etc. Other important question os how we decide how long a generated string should be. How do we specify this? Can we specify this on the fly through the discord bot?

