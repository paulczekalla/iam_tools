import json
import copy
from lib.auth import Auth, AuthException
from lib.httpHandler import HttpHandler
from lib.fileWriter import FileWriter

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

gf_exclude = [
  {"id":157247, "action":"exclude"},
  {"id":157248, "action":"exclude"},
  {"id":157249, "action":"exclude"},
  {"id":157250, "action":"exclude"},
  {"id":166927, "action":"exclude"},
  {"id":166919, "action":"exclude"},
]


filename = "deleted_campaigns.csv"

http = HttpHandler(proxies)

a = Auth("a", "b")

aquireAuthToken(a, http)

campaigns = (1701805, 1708798, 1708806, 1708809, 1897308, 2073890, 2073895, 2304760, 2060424, 2179732, 2179739, 2179744, 2315824, 2060427, 2179676, 2179677, 2179710, 2315881, 2089891, 2109582, 2109589, 2109590, 2109591, 2109594, 2109595, 2109596, 2490460, 2393074, 2406706, 2406707, 2406708, 2406712, 2406713, 2406715, 2509665, 2509666, 2509667, 2509668, 2509669, 2509670, 2509671, 2509672, 2509673, 2509674, 2509676, 2509678, 2509680, 2509681, 2509682, 2509683, 2509685, 2528908, 2528910, 2528911, 2528912, 2528913, 2528914, 2528915, 2528916, 2528917, 2528918, 2528919, 2528920, 2528921, 2528925, 2528928, 2528930, 2528932, 2528935, 2556469, 2556921, 2556963, 2557122, 2557124)

filename = "log_updated_campaigns.csv"

writer_content = list()
writer_content.append('Id;Name;Status;Publisher Targets; Old Targets\n')

for campaign_id in campaigns:
	params = {'id':str(campaign_id)}
	campaign = http.getRequest("campaign", params).json()['response']['campaign']
	params = {'id':str(campaign['profile_id'])}
	profile = http.getRequest("profile", params).json()['response']['profile']
	
	publisher_exclude = list(gf_exclude)
	old_targets = ""
	if profile['publisher_targets'] is not None:
		for target in profile['publisher_targets']:
			publisher_exclude.append(target)
			old_targets += str(target) + ' '
			
	
	payload = {"profile":{"publisher_targets":publisher_exclude}}
	publisher_targets = payload
	status = http.putRequest(payload, "profile", params).json()['response']['status']
	writer_string = str(campaign_id) + '; ' + campaign['name'] + '; ' + status + ';' + str(publisher_exclude) + '; ' + old_targets + '\n'
	writer_content.append(writer_string)

fw = FileWriter(filename, 'w')

for line in writer_content:
	fw.writeInNewFile(line)

fw.closeFile()
