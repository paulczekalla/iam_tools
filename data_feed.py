﻿import json
from lib.auth import Auth,AuthException

from lib.httpHandler import HttpHandler
from worker.siphon.feedGenerator import FeedGenerator
from worker.siphon.SiphonDownloader import SiphonDownloader

def aquireAuthToken(authObj, http):
	token = ""
	try:
		token = authObj.readResponse(authObj.authorizationRequest(http))
	except AuthException as e:
		print("Login mit Zugang {} nicht möglich.".format(e.login))
		print("Zugangsdaten erneut eingeben: ")
		login = input("Login: ")
		password = input("Passwort: ")
		aquireAuthToken(Auth(login, password), http)
	else:
		http.setToken(token)

http = HttpHandler()

a = Auth("a", "b")
aquireAuthToken(a, http)

feedTypes = ("segment_feed")

allDataFeeds = FeedGenerator(http, feedTypes)
downloader = SiphonDownloader("temp", http)
download_links = allDataFeeds.generateLocationRequests(allDataFeeds.getFeeds())
for params in download_links:
	downloader.download_file(params)
