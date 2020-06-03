# Argus Message Notifier
Copyright (C) 2020 Beqa Gozalishvili

Notifies about unread messages from argus iliauni portal in telegram.

## requirements
* BeautifulSoup
* requests

pip install bs4 requests

## Usage
1. Open chat with BotFather and create a new telegram bot.
2. save api token after successfull bot creation.
3. Start chat with your newly created bot and write some message to it.
4. send a request in the following form: https://api.telegram.org/bot<bottoken>/getUpdates.
5. save chat id from json response.

Create a file called constants.py in script directory and put credentials in the following form

* tBotToken = "botToken"
* tChatID = chatID
* login = "argusLogin"
* password = "argusPassword"

## Contributions
If you found a bug or have a suggestion, please open an issue or pr.