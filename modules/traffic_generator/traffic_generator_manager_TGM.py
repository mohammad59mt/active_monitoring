from flask import Flask, json,request
#from utilities import Rest
import asyncio

import logging
import threading
import time
from multiprocessing import Process
import multiprocessing

manager = multiprocessing.Manager()
end_to_end_delay_for_all_agents = manager.dict()

api = Flask(__name__)

__agent_listen_port =5000

import http,http.client
import json
class Rest():
    """
    This class is implemented to do Rest Client tasks
    """
    def __init__(self, server,port,path):
        self.server = server
        self.port = port
        self.path = path
  
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2].decode('utf-8'))
  
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        print ("set ret: ",ret)
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
        conn.close()
        return ret

def start_agent_traffic(name, agent_ip, agent_port, dst_ips_matrix):
    r = Rest(agent_ip,agent_port,'/traffic/agent/start')
    hosts_resp, return_data = r.set(dst_ips_matrix)
    end_to_end_delay_for_all_agents[agent_ip]=return_data

def start_traffic_on_all_agents(traffic_pattern):
    thread_name = 0
    lst_process=[]

    for agent_ip in traffic_pattern:
        thread_name=thread_name+1
        tmp_proc = Process(target=start_agent_traffic, args=(thread_name,agent_ip,__agent_listen_port,traffic_pattern[agent_ip],))
        tmp_proc.start()
        lst_process.append(tmp_proc)

    for proc in lst_process:
        proc.join() #waint until all threads finish

@api.route('/traffic/manager/start', methods=['POST'])
def post_traffics():
    traffic_pattern = request.get_json()

    start_traffic_on_all_agents(traffic_pattern)
    global end_to_end_delay_for_all_agents

    return json.dumps(end_to_end_delay_for_all_agents.copy()), 201

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    import json
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='This script is for running packet generator manager on desired host. This manager recieves commands via rest api from the coordinator.')
    parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
    parser.add_argument('--port', dest='port', help="Listen port.")

    args = parser.parse_args()
    config_file_path             = args.config_file_path
    listen_port                  = args.port  

    if config_file_path != None:
        with open(config_file_path) as config_file:
            data = json.load(config_file)

        if listen_port == None:
            if 'traffic_manager' in data and 'port' in data['traffic_manager']:
                listen_port=data['traffic_manager']['port']
            else:
                listen_port=5000
        
        if 'agents' in data and 'port' in data['agents']:
            __agent_listen_port = data['agents']['port']
        else:
            __agent_listen_port = 5000


    api.run(host="0.0.0.0",port=listen_port)