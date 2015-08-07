'''
Created on 29 Jul 2015

@author: bernie.kim
'''

from suds.client import Client

class Auth:
    '''
    classdocs
    '''

    def __init__(self, username, password, appkey, url):
        self.username = username
        self.password = password
        self.appkey = appkey
        self.url = url
        
        client = Client(url, faults = False)
        response = client.service.ClientLogin(username, password, appkey)
        
        self.code = response[0]
        if response[0] == 200:
            self.token = response[1]
        else:
            self.token = None
        
    def getStatus(self):
        return self.code

