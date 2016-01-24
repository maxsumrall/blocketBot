__author__ = 'Max'

import re
import threading
import time

import requests
import telegram
from bs4 import BeautifulSoup

observedHouses = {}
conversations = {}
url = ""
telegram_bot_token = ""
bot = None


def getHTML(url):
    request = requests.get(url)
    htmlData = request.text
    return htmlData


def extractListings(htmlData):
    soup = BeautifulSoup(htmlData, "html.parser")
    listings = soup.findAll(
            lambda tag: tag.name == "div" and
                        "itemtype" in tag.attrs and
                        "Offer" in tag.attrs["itemtype"])
    firstRun = False
    if len(observedHouses) == 0:
        firstRun = True
    for house in listings:
        houseItemChild = [x for x in list(house.children) if (hasattr(x, "tags") and "media-body" in x['class'])]
        houseDetails = [x for x in list(houseItemChild[0].children) if (hasattr(x, "tags") and "details" in x['class'])]
        price = [x for x in list(houseDetails[0].children) if (hasattr(x, "tags") and "monthly_rent" in x["class"])]
        if (len(price) < 1):
            continue

        numPrice = re.sub("[^0-9]", "", price[0].text.split("kr")[0])
        houseURL = house.a.attrs['href']

        key = numPrice + houseURL

        if key not in observedHouses:
            observedHouses[key] = {'price': numPrice,
                               'url': houseURL}
            if not firstRun:
                sendTelegram(numPrice, houseURL)


def sendTelegram(price, url):
    updateConversations()
    for chatIDs in conversations.keys():
        bot.sendMessage(chat_id=chatIDs, text="A new listing has been posted! Price: " + price + "kr,  URL: " + url)


def updateConversations():
    for update in bot.getUpdates():
        conversations[update.message.chat_id] = True


def startupMessage():
    for chatIDs in conversations.keys():
        bot.sendMessage(chat_id=chatIDs, text="HouseBot is up and running")


def parseConfig():
    print "Opening config file: config.txt"
    try:
        configFile = open("config.txt", "r")
        parsed_url = configFile.readline().split("=")
        if ((parsed_url[0] != "listings_url") or (parsed_url[1] == "")):
            print "The URL to parse was not found in the configuration file."
            exit()
        telegramToken = configFile.readline()
        if ((telegramToken[0] != "telegram_token") or (telegramToken[1] == "")):
            print "The telegram token was not found in the configuration file."
            exit()

        global url, telegram_bot_token
        url = parsed_url[1]
        telegram_bot_token = telegramToken[1]

    except:
        print "An error occured while parsing the configuration file: config.txt. "


def initTelegramBot():
    global bot, telegram_bot_token
    bot = telegram.Bot(token=telegram_bot_token)


def update():
    print "updated " + str(time.ctime())
    extractListings(getHTML(url))
    threading.Timer(180.0, update).start()


def main():
    parseConfig()
    updateConversations()
    startupMessage()
    update()


main()
