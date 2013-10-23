from time import time
import sys

class Auth:

	def __init__(self, username="", password=""):
		self._username = username
		self._password = password
	
		self.http = None
		self.auth_data = None
		
		self.createCredentialJson()

		
	def __str__(self):
		return "Login: " + self._username + "\nPassword: " + self._password
	
	def setUsername(self, username):
		self._username = username
	
	def getUsername(self):
		return self._username

	username = property(getUsername, setUsername)
	
	def setPassword(self, password):
		self._password = password
			
	def getPassword(self):
		return self._password
	
	password = property(getPassword, setPassword)
	
	def createCredentialJson(self):
		self.auth_data = {"auth":{"username":self._username,"password":self._password}}
	
	def authorizationRequest(self, http=None):
		if http is not None:
			self.http = http
		self.http._baseUrl="http://api.appnexus.com"
		self.http._service="auth"
		return self.http.postRequest(self.auth_data)

	def readResponse(self, r):
		response_json = r.json()['response']
		if 'error' not in response_json:
			if response_json['status'] == "OK":
				return (response_json['token'])
			else:
				print("Something went wrong. Check Auth Module")
		else:
			if 'No match found for user/pass' in response_json['error']:
				print('Wrong credentials. Exiting program.')
				sys.exit(0)
			else:
				print("Auth again in 15 seconds")
				time.sleep(15)
				self.readResponse(self.authorizationRequest())
			
