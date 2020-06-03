#ArgusMessageNotifier.py
# Copyright (C) 2020 beqa gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from bs4 import BeautifulSoup
from constants import *
from functools import wraps
import json
import re
import requests
from requests.exceptions import RequestException
import sys
import threading
import time
import winsound

baseUrl = "https://argus.iliauni.edu.ge/ka/"
tBotUrl = "https://api.telegram.org/bot"

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
	def func(f):
		@wraps(f)
		def f_retry(*args, **kwargs):
			mtries, mdelay = tries, delay
			while mtries > 1:
				try:
					return f(*args, **kwargs)
				except ExceptionToCheck as e:
					msg = f"an exception has occurred: {e}, trying to connect in {mdelay} seconds..."
					print(msg)
					time.sleep(mdelay)
					mtries -= 1
					mdelay *= backoff
			return f(*args, **kwargs)
		return f_retry
	return func

@retry((RequestException), tries=20, delay=10, backoff=1)
def makeRequest(method, url, data=None, session=None):
	if session:
		res = session.request(method, url, data=data)
	else:
		res = requests.request(method, url, data=data)
	return res

def prettifyString(text):
	return text.lstrip().replace("\n", "")

def authorize(login, password):
	mPage = makeRequest("GET", baseUrl, session=session)
	token = re.search('_token" value="(.*)">', mPage.text).groups(1)
	return makeRequest("POST", f"{baseUrl}login", data={"_token":token, "login":login, "password":password}, session=session)

def getMessagesCount():
	return makeRequest("GET", f"{baseUrl}student/messages/get-unread-count", session=session).json()['count']

def getMessages():
	messages = []
	messagesInbox = makeRequest("GET", f"{baseUrl}student/messages/inbox", session=session)
	soup = BeautifulSoup(messagesInbox.content, 'html.parser')
	table = soup.find("table")
	rows = table.findAll("tr")
	for row in rows[2:]:
		messageLink = row.findAll("td")[2].find("a")["href"]
		messageReq = makeRequest("GET", messageLink, session=session)
		msg = BeautifulSoup(messageReq.content, 'html.parser')
		messageBlock = msg.findAll("div", class_="card")[3]
		author = prettifyString(messageBlock.findAll('h4')[0].text)
		date = prettifyString(messageBlock.findAll('h4')[1].text)
		subject = prettifyString(messageBlock.find("h5").text)
		text = prettifyString(messageBlock.find("div", class_="card-body").text)
		message = {"author": author, "date": date, "subject": subject, "text": text}
		messages.append(message)
	return messages

def main():
	messageCount = getMessagesCount()
	print(f"You have {messageCount} new messages.")
	if messageCount == 0:
		pass
	else:
		winsound.PlaySound("argusAlert.wav", winsound.SND_FILENAME)
		messages = getMessages()
		for message in getMessages():
			text = f"""
from: {message['author']}
subject: {message['subject']}
message: {message['text']}
received on: {message['date']}
"""
			print(text)
			resp = makeRequest("GET", f"{tBotUrl}{tBotToken}/sendMessage?chat_id={tChatID}&text={text}")
	#timer = threading.Timer(600, main)
	#timer.start() 
	time.sleep(600)

session = requests.session()
authorize(login, password)
while True:
	main()
