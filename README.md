# Blocket Bot

A python script to check the Swedish second-hand market site Blocket.se for new house or apartment listings.

This sends you a telegram message whenever a new listing is posted. To use it you need your own telegram
bot, which you can create using the [Telegram BotFather](https://core.telegram.org/bots). Once you make a bot, start 
a conversation with the bot and wait for new listings to be posted.

# Config
The program expects a file called `config.txt` and looks exactly like `example_config.txt` but with your telegram bot 
API key and the url of the blocket page you want the bot to watch. Use the URL in the example config file to see what
page you should be giving the program to check. 

# How to use

You need [Python 2.7](https://www.python.org/downloads/) and the [pip package manager](https://pip.pypa.io/en/stable/quickstart/).

You then need to install a [wrapper for the telegram API](https://pypi.python.org/pypi/python-telegram-bot/3.2.0) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/).
```sh
$ pip install beautifulsoup4
$ pip install python-telegram-bot
```

That's it! Start the bot up!
```sh
$ screen
$ python blocketBot.py
```

# Other uses
This project is just a screen scraper that uses the telegram API. Take a look, it's only 100 lines. You can use this 
for scraping some other sites on blocket or just to see an example of how easy it is to make a telegram bot. 


This project is licensed under the terms of the [GPL license](http://www.gnu.org/licenses/gpl-3.0.txt).