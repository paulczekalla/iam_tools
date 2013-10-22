import json
from lib.auth import Auth
from lib.httpHandler import HttpHandler
from worker.siphon.feedGenerator import FeedGenerator
from worker.siphon.SiphonDownloader import SiphonDownloader

http = HttpHandler()
a = Auth("auth", "here")

token = a.readResponse(a.authorizationRequest(http))
http.setToken(token)

allDataFeeds = FeedGenerator(http)
downloader = SiphonDownloader("temp", http)
download_links = allDataFeeds.generateLocationRequests(allDataFeeds.getFeeds())
for params in download_links:
	downloader.download_file(params)
