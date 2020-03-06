import http,http.client

import json



'''

This class is implemented to do Rest Client tasks

'''

class Rest():

    def __init__(self, server,port,path):

        self.server = server

        self.port = port

        self.path = path

  

    def get(self, data):

        ret = self.rest_call({}, 'GET')

        return json.loads(ret[2].decode('utf-8'))

  

    def set(self, data):

        ret = self.rest_call(data, 'POST')

        returned_data = json.loads(ret[2].decode('utf-8'))

        return ret[0] == 201, returned_data



  

    def remove(self, objtype, data):

        ret = self.rest_call(data, 'DELETE')

        return ret[0] == 200

  

    def rest_call(self, data, action):

        path = self.path

        headers = {

            'Content-type': 'application/json',

            'Accept': 'application/json',

            }

        body = json.dumps(data)

        conn = http.client.HTTPConnection(self.server, self.port)

        conn.request(action, path, body, headers)

        response = conn.getresponse()

        ret = (response.status, response.reason, response.read())

        #print (ret)

        conn.close()

        return ret