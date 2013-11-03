import json
import requests
from lib.auth import Auth,AuthException

from lib.httpHandler import HttpHandler
from worker.generic.AbstractGenericWorker import AbstractGenericWorker

def aquireAuthToken(authObj, http):
	token = ''
	try:
		token = authObj.readResponse(authObj.authorizationRequest(http))
	except AuthException as e:
		print('Login mit Zugang {} nicht möglich.'.format(e.login))
		print('Zugangsdaten erneut eingeben: ')
		login = input('Login: ')
		password = input('Passwort: ')
		aquireAuthToken(Auth(login, password), http)
	else:
		print(token)
		http.setToken(token)

http = HttpHandler()

a = Auth('Auth', 'here')
aquireAuthToken(a, http)

worker = AbstractGenericWorker(http)

placements = worker.getAllEntitiesByType('placement')

for place in placements:
	print(str(place['id']) + ' ' + str(place['site_id']))
	hex_id = str(hex(place['site_id'])).split("0x")[1]
	print("www.interactivemedia-" + str(hex_id) + ".net")

payload = {"placement":{"default_referrer_url":None}}

params = {'id':placements[3]['id']}
reqRet = http.putRequest(payload, 'placement', params)
print(reqRet.json()['response']['status'])
