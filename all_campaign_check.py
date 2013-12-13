import json
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter
from worker.allLineitemCheck.allLineitemsCheck import AllLineitemsCheck

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

proxies = {
  "http": "http://proxy.t-online.net:3128",
  "https": "http://proxy.t-online.net:3128",
}

filename = "all_campaign_date.csv"

http = HttpHandler(proxies)

a = Auth("a", "b")

aquireAuthToken(a, http)

count = http.getRequestPage(0, "campaign").json()['response']['count']

allLineItems = list()

for start_element in range(0, count, 100):
	resp = http.getRequestPage(start_element, "campaign").json()['response']
	if 'error_id' in resp:
		print(resp)
	else:
		allLineItems.append(resp['campaigns'])

allLineitems = AllLineitemsCheck()

writer_content = list()
writer_content.append('Id;Name;LastMod;\n')

# Low running items
writer_content.append('\n')
writer_content.append('All Lineitems \n')
writer_content.append('\n')

for lineItem in allLineitems.get_all_items(allLineItems):
	line = str(lineItem['id']) + ';' + lineItem['name'] + ';'
	if lineItem['last_modified'] is not None:
		line += lineItem['last_modified'].split(" ")[0] + '\n' 
	
	writer_content.append(line)

fw = FileWriter(filename, 'w')

for line in writer_content:
	print(line)
	print("---")
	fw.writeInNewFile(line)

fw.closeFile()
