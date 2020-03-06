#from utilities import Rest
import pprint
import http,http.client

import json
  
__controller_ip = '192.168.100.230'
__controller_port = 8080

# __topology_graph = {}
# __topology_links = {}
  
coordinator_and_manager_sw_dpid ='00:00:00:00:00:00:f0:00' #todo config.
### https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html

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

        #print (ret)

        conn.close()

        return ret



class ControllerApi (object):
    def __init__(self,controller_ip,controller_port):
        self.__controller_ip = controller_ip
        self.__controller_port = controller_port
        self.__topology_graph = {}
        self.__topology_links = {}
        self.__topology_hosts_IP_to_MAC_map = {}
        self.__topology_hosts_MAC_to_IP_map = {}

    def __get_switches (self):
        r = Rest(self.__controller_ip,self.__controller_port,'/wm/core/controller/switches/json')
        topo = r.get({})
        switches = []
        number_of_valid_detected_switches = 0
        
        for i in range(0,len(topo)):
            if topo[i]['switchDPID']!=coordinator_and_manager_sw_dpid:
                #del topo[i]
                switches.append(topo[i]['switchDPID'])
                number_of_valid_detected_switches+=1

        for sw1 in switches:
            for sw2 in switches:
                self.__topology_graph[(sw1,sw2,'s')]=0
                    
        print ("debug: Number of valid detected switches by controller: ",number_of_valid_detected_switches)

        return switches

    def __get_links (self):
        r = Rest(self.__controller_ip,self.__controller_port,'/wm/topology/links/json')
        links_resp = r.get({})
        links = []
        result_graph={}
        for link in links_resp:
            src_dpid = link['src-switch']
            src_port = link['src-port']
            dst_dpid = link['dst-switch']
            dst_port = link['dst-port']
            if src_dpid!=coordinator_and_manager_sw_dpid and dst_dpid!=coordinator_and_manager_sw_dpid:
                #print ("src_dpid: ",src_dpid)
                #print ("dst_dpid: ",dst_dpid)
                #print ("coordinator_and_manager_sw_dpid: ",coordinator_and_manager_sw_dpid)
                self.__topology_graph[(src_dpid,dst_dpid,'s')]+=1
                self.__topology_links[(src_dpid,dst_dpid,'s')]=(src_port,dst_port)
                self.__topology_graph[(dst_dpid,src_dpid,'s')]+=1
                self.__topology_links[(dst_dpid,src_dpid,'s')]=(dst_port,src_port)
        #return links

    def __get_hosts (self):
        r = Rest(self.__controller_ip,self.__controller_port,'/wm/device/')
        hosts_resp = r.get({})
        number_of_valid_detected_hosts = 0
        for host in hosts_resp['devices']:
            host_mac = host['mac'][0]            
            if len(host['ipv4']) >0:
                host_ip = host['ipv4'][0]
            else:
                continue
            #print (host)
            try:
                switch_dpid = host['attachmentPoint'][0]['switch']
                switch_port = host['attachmentPoint'][0]['port']
                if switch_dpid!=coordinator_and_manager_sw_dpid:
                    #self.__topology_graph[(host_mac,switch_dpid,'h')]=1
                    self.__topology_graph[(host_ip, switch_dpid, 'h')] = 1
                    #self.__topology_links[(host_mac,switch_dpid,'h')]=(host_ip,switch_port)
                    self.__topology_links[(host_ip, switch_dpid, 'h')] = (host_mac, switch_port)
                    self.__topology_hosts_IP_to_MAC_map[host_ip]=host_mac
                    self.__topology_hosts_MAC_to_IP_map[host_mac]=host_ip
                    number_of_valid_detected_hosts+=1
            except :
                print ("Exception")
            
        print ("debug: Number of valid detected hosts by controller: ",number_of_valid_detected_hosts)
        return hosts_resp['devices']

    def get_topo_from_controller(self):
        global __topology_graph
        self.__get_switches()
        self.__get_links()
        self.__get_hosts()
        return self.__topology_graph,self.__topology_links,self.__topology_hosts_IP_to_MAC_map,self.__topology_hosts_MAC_to_IP_map

    def add_flow(self,in_port,dpid,ipv4_src,ipv4_dst,out_port,ip_protocol,ip_tos,set_eth_src="",set_eth_dst="",set_ipv4_src="",set_ipv4_dst="",priority=32768):
        dpid_int = int(str.encode(dpid).translate(None,b":"), 16)
        flow={}
        from random import randint,seed
        if set_eth_src=="" and set_eth_dst=="" and set_ipv4_src=="" and set_ipv4_dst=="":
            flow={
            "switch":str(dpid),
            "name":str(randint(0,100))+"_"+str(dpid_int)+"_"+str(in_port)+"_"+str(out_port)+"_"+str(ip_tos),
            "cookie":"0",
            "priority":str(priority),
            "in_port":str(in_port),
            "eth_type":"0x800",
            "ipv4_src":ipv4_src,
            "ipv4_dst":ipv4_dst,
            "ip_proto": ip_protocol,
            "ip_tos":str(ip_tos),
            "active":"true",
            "actions":"output="+str(out_port)
            }
        elif set_eth_src!="" and set_eth_dst!="" and set_ipv4_src!="" and set_ipv4_dst!="" :
            #set_field=arp_tpa->10.0.0.2
            actions="set_field=eth_src->%s,set_field=eth_dst->%s,set_field=ipv4_src->%s,set_field=ipv4_dst->%s,set_field=icmpv4_type->%s,output=%s"%(set_eth_src,set_eth_dst,set_ipv4_src,set_ipv4_dst,0,out_port)
            flow={
            "switch":str(dpid),
            "name":str(randint(0,100))+"_"+str(dpid_int)+"_"+str(in_port)+"_"+str(out_port)+"_"+str(ip_tos)+"2_"+str(randint(0,100)),
            "cookie":"0",
            "priority":str(priority),
            "in_port":str(in_port), 
            "eth_type":"0x800",
            "ipv4_src":ipv4_src,
            "ipv4_dst":ipv4_dst,
            "ip_proto": ip_protocol,
            "ip_tos":str(ip_tos),           
            "active":"true",
            "instruction_apply_actions":actions
            }
            #"actions":actions
            #"actions":"output=+str(out_port)+","+"set_eth_src='"+str(set_eth_src)+"',"+"set_eth_dst='"+str(set_eth_dst)+"',"+"set_ipv4_src='"+str(set_ipv4_src)+"',"+"set_ipv4_dst='"+str(set_ipv4_dst)+"'"%()
        else:
            print("unable to push flow: ",flow)
            return
        #print (flow)

        r = Rest(self.__controller_ip,self.__controller_port,'/wm/staticentrypusher/json')
        resp = r.set(flow)

        if 'status' in resp[1]:
            return resp[1]['status'] == 'Entry pushed',flow
        else:
            return False,""


    
if __name__=='__main__':
    a = ControllerApi("127.0.0.1",8080)
    b,c,d,e =a.get_topo_from_controller()
    pp = pprint.PrettyPrinter(depth=2)

    pp.pprint (c)


    # in_port=1
    # out_port=2
    # dpid="00:00:00:00:00:00:00:01"
    # ip_tos=1
    # ip_proto = "0x01" #icmp
    # ok = add_flow(in_port=in_port,dpid=dpid,out_port=out_port,ip_proto=ip_proto,ip_tos=ip_tos)
    # if ok == True:
    #     print ("Entry Pushed!")

    #get_topo_from_controller()
    #pp = pprint.PrettyPrinter(depth=2)
    #pp.pprint(__topology_graph)
    ###print (__topology_graph)
    #print (__topology_links)
    ###print ("\n\n")
    #pp.pprint (__get_hosts())
    #pp.pprint(__topology_links)
    #add_flow(1,int('0000000000000001'),2)
    #print (topology_graph)
