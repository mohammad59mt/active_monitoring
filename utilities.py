from modules.sdn_applications.floodlight.rest_client_for_floodlight import ControllerApi as FloodlightAPI
from threading import Thread


## JSON Pretty Printer
import pprint


PG_manager_ip = "10.0.0.202"
PG_manager_port = 5000
PG_manager_port_test = 5050

controller_ip = "10.0.0.200"
# controller_ip = "192.168.254.128"
# controller_ip = "127.0.0.1"
controller_port = 8080

helperIPAddress = "10.0.0.250"
helperMACAddress = "00:00:00:00:00:fa"

pp = pprint.PrettyPrinter(depth=2)

test_hosts_last_octet_is_greater_than = 100

import logging
logger= logging.getLogger( __name__ )


class TopoInteractions:
    def __init__(self):
        self.ipToMACAddressMap = {}
        self.MACtoIPAddressMap = {}
        self.ipToMACAddressMap[helperIPAddress] = helperMACAddress
        self.MACtoIPAddressMap[helperMACAddress] = helperIPAddress
        self.topo_links = {}

    def __convert_pathes_to_route(self,path):
        '''
        path= [
            ['10.0.0.1','00:00:00:00:00:00:00:01','00:00:00:00:00:00:00:02','10.0.0.2'],
            ['10.0.0.2','00:00:00:00:00:00:00:02','00:00:00:00:00:00:00:03','10.0.0.3']
        ]

        route=[
            ['10.0.0.1',('s1-eth1','00:00:00:00:00:00:00:01','s1-eth2'),('s2-eth1','00:00:00:00:00:00:00:02','s2-eth4'),'10.0.0.2'],
            ['10.0.0.2',('s2-eth4','00:00:00:00:00:00:00:02','s2-eth3'),('s3-eth1','00:00:00:00:00:00:00:03','s3-eth2'),'10.0.0.3']
        ]
        '''
        route = [None] * len(path)
        for i in range(0, len(path)):
            route[i] = [None] * len(path[i])
    
            for j in range(0, len(path[i])):
                if j == 0 or j == len(path[i]) - 1:
                    route[i][j] = path[i][j]
                    continue

                if j == 1:
                    in_port = self.topo_links[(path[i][j - 1], path[i][j], 'h')][1]
                    out_port = self.topo_links[(path[i][j], path[i][j + 1], 's')][0]
                elif j == len(path[i]) - 2:
                    out_port = self.topo_links[(path[i][j + 1], path[i][j], 'h')][1]
                    in_port = self.topo_links[(path[i][j], path[i][j - 1], 's')][0]
                else:
                    in_port = self.topo_links[(path[i][j - 1], path[i][j], 's')][1]
                    out_port = self.topo_links[(path[i][j], path[i][j + 1], 's')][0]

                if in_port == out_port:
                    # ref:https://mailman.stanford.edu/pipermail/openflow-discuss/2015-April/005636.html
                    out_port = "in_port"
                route[i][j] = (in_port, path[i][j], out_port)
        return route

    def push_flows(self,pathes, interval=0.005,simulation=False,debug=False):
        """
        pathes = 
        [
            ['10.0.0.1',('s1-eth1','00:00:00:00:00:00:00:01','s1-eth2'),('s2-eth1','00:00:00:00:00:00:00:02','s2-eth4'),'10.0.0.2'],
            ['10.0.0.2',('s2-eth4','00:00:00:00:00:00:00:02','s2-eth3'),('s3-eth1','00:00:00:00:00:00:00:03','s3-eth2'),'10.0.0.3']
        ]

        simulation: if true just rules will be created and won't be installed really on switches

        list_of_traffic_pattern=
        {
            "'10.0.0.1'":[
                {"dst_ip":"'10.0.0.2'","ip_tos":"1","ip_protocol":"icmp"},
                {"dst_ip":"'10.0.0.3'","ip_tos":"1","ip_protocol":"icmp"}
            ]
        }  
        """
        path_detector = {}  # path_detector[(src_host_ip,dst_host_ip)] = path_number

       

        '''count number of pathes between host couples'''
        pathes = self.__convert_pathes_to_route(pathes)

        global helperIPAddress

        for path in pathes:
            if debug: logger.debug (path)           
            src_host_ip = path[0]
            dst_host_ip = path[-1]

            # Some traffics are from same source and destination, So it's need to handle this case. We used a helperIPAddress to force traffic to get outside of that host and then manage it by changing ip address at last switch and also change icmp type.
            if src_host_ip == dst_host_ip:
                path = _replace_dst_ip_with_helper_ip_address(path)
                dst_host_ip = helperIPAddress

            if (src_host_ip, dst_host_ip) not in path_detector:
                path_detector[(src_host_ip, dst_host_ip)] = 1

            else:
                path_detector[(src_host_ip, dst_host_ip)] += 1

        flows = []  # for debug
        controller_api = FloodlightAPI(controller_ip, controller_port)

        check_last_rule_added = set()  #flow table entries optimization

        # for path in pathes:
        for j in range(0, len(pathes)):
            src_host_ip = pathes[j][0]
            dst_host_ip = pathes[j][-1]

            ip_tos = path_detector[(src_host_ip, dst_host_ip)]
            path_detector[(src_host_ip, dst_host_ip)] = path_detector[
                                                            (src_host_ip, dst_host_ip)] - 1  # consume path detector
            for i in range(1, len(pathes[j]) - 1):
                in_port = pathes[j][i][0]
                out_port = pathes[j][i][2]
                dpid = pathes[j][i][1]
                ip_protocol = "0x1"

                
                if i != len(pathes[j]) - 2:
                    if not simulation:
                        ok, flow = controller_api.add_flow(in_port, dpid, src_host_ip, dst_host_ip, out_port, ip_protocol,ip_tos)
                        from time import sleep
                        sleep(interval)
                    flows.append(flow)

                else:
                    if src_host_ip in check_last_rule_added:
                        continue
                    check_last_rule_added.add(src_host_ip)
                    # if dpid==nat_switch_dpid and i==len(path)-2: #last switch
                    # swap dst_ip with src_ip  and dst_eth with src_eth
                    set_ipv4_src = dst_host_ip
                    set_ipv4_dst = src_host_ip
                    set_eth_src = helperMACAddress
                    set_eth_dst = self.ipToMACAddressMap[pathes[j][0]]

                    # change icmp_type from 8 to 0 leads to convert icmp echo request to icmp echo reply
                    # icmpv4_type  = 0
                    in_port = 0
                    ip_tos = 0
                    if not simulation:
                        ok, flow = controller_api.add_flow(
                            in_port,
                            dpid, 
                            src_host_ip,
                            helperIPAddress,
                            out_port,
                            ip_protocol,
                            ip_tos ,
                            set_eth_src,
                            set_eth_dst,
                            set_ipv4_src,
                            set_ipv4_dst,
                            priority=32768
                        )
                        from time import sleep
                        sleep(interval)

                    flows.append(flow)
                    
                if ok != True:
                    return False,flows

                path = _replace_dst_ip_with_helper_ip_address(path)

        return True,flows

def add_dic_to_file(dic,filepath):
    f = open(filepath, "w+")
    f.write(str(dic))
    f.close()

def load_dic_from_file(filepath):
    f = open(filepath, "r+")
    dic = eval(f.read())
    f.close()
    return  dic

def __convert_to_colon_separated (a):
    #a = "0000000000000001"
    for j in range(0, int(len(a) / 2)):
        if j == 0:
            continue
        a = a[0:2 * j + j - 1] + ":" + a[2 * j + j - 1:]
    # a = "00:00:00:00:00:00:00:01"
    return a

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def delete_test_hosts_from_topo_matrix(topo_matrix,test_hosts_last_octet_is_greater_than):
    contain_host=False
    for k in list(topo_matrix):
        #print(k[2])
        if k[2]=='s':
            continue
        if k[2] == 'h':
            contain_host=True

        last_octet = int(k[0].split(".")[3])

        if int(k[0].split(".")[3]) > test_hosts_last_octet_is_greater_than:
            del (topo_matrix[k])
    return topo_matrix,contain_host

def __convert_sw_dpid_to_host_ip(dpid):
    first_sw_id = int(dpid.split(":")[-1], 16)
    first_host_id = first_sw_id
    if first_sw_id < 10:
        first_host_id = "0" + str(first_sw_id)
    first_host_ip = "10.0.0.1" + str(first_host_id)

    return first_host_ip

def convert_host_ip_to_sw_dpid(ip):
    #ip = "10.0.0.101"
    dpid = "00:00:00:00:00:00:00:"
    last_octet = int(ip.split(".")[3])

    if last_octet>100:
        last_octet = last_octet-100
    if last_octet<16:
        #last_octet = str(last_octet)
        dpid = dpid+"0"+str(hex(last_octet).lstrip('0x'))
    else:
        #last_octet = str(last_octet)
        dpid = dpid+str(hex(last_octet).lstrip('0x'))
    return dpid

def get_test_hosts_traffic_pattern_from_link_info(topo_links):
    test_host_traffic_dict = {}  # {"10.0.0.101":["10.0.0.102","10.0.0.103"]}
    for k in list(topo_links):
        if k[2] == 's':
            first_host_ip = __convert_sw_dpid_to_host_ip(k[0])
            second_host_ip = __convert_sw_dpid_to_host_ip(k[1])
            if first_host_ip not in test_host_traffic_dict:
                test_host_traffic_dict[first_host_ip]=[]
            test_host_traffic_dict[first_host_ip].append({"dst_ip":second_host_ip})
           # test_host_traffic_list.append((first_host_ip, second_host_ip))
    return test_host_traffic_dict

def __send_traffic_pattern_to_traffic_manager(list_of_traffic_pattern,ip,port):
    """
    coord_h curl -XPOST '10.0.0.20'2:5001/traffic/manager/start --header 'Content-Type: application/json' -d '{"'10.0.0.1'":[{"dst_ip":"'10.0.0.2'","ip_tos":"1","ip_protocol":"0x1"},{"dst_ip":"'10.0.0.3'","ip_tos":"1","ip_protocol":"0x1"}],"'10.0.0.2'":[{"dst_ip":"'10.0.0.1'","ip_tos":"1","ip_protocol":"0x1"},{"dst_ip":"'10.0.0.3'","ip_tos":"1","ip_protocol":"0x1"}]}'
    """
    r = Rest(ip, port, '/traffic/manager/start')
    hosts_resp, return_data = r.set(list_of_traffic_pattern)
    return return_data

def generate_flows_to_test_hosts(dict_of_test_hosts_traffic_pattern):
    """
    dict_of_test_hosts_traffic_pattern =
    {"10.0.0.101":[{"dst_ip":"10.0.0.102"},{"dst_ip":"10.0.0.103"}}
    list_of_traffic_pattern=
    {
        "10.0.0.1":[
            {"dst_ip":"10.0.0.2","ip_tos":"1","ip_protocol":"0x1"},
            {"dst_ip":"10.0.0.3","ip_tos":"1","ip_protocol":"0x1"}
        ]
    }

    """
    global PG_manager_ip, PG_manager_port_test
    return __send_traffic_pattern_to_traffic_manager(
        dict_of_test_hosts_traffic_pattern,PG_manager_ip,PG_manager_port_test), dict_of_test_hosts_traffic_pattern

def generate_flows(pathes):


    
    """
    pathes = 
    [
        ['10.0.0.1',('s1-eth1','00:00:00:00:00:00:00:01','s1-eth2'),('s2-eth1','00:00:00:00:00:00:00:02','s2-eth4'),'10.0.0.2'],
        ['10.0.0.2',('s2-eth4','00:00:00:00:00:00:00:02','s2-eth3'),('s3-eth1','00:00:00:00:00:00:00:03','s3-eth2'),'10.0.0.3']
    ]
    list_of_traffic_pattern=
    {
        "10.0.0.1":[
            {"dst_ip":"10.0.0.2","ip_tos":"1","ip_protocol":"0x1"},
            {"dst_ip":"10.0.0.3","ip_tos":"1","ip_protocol":"0x1"}
        ]
    }  

    """
    length = len(pathes)
    path_detector = {}  # path_detector[(src_host_ip,dst_host_ip)] = path_number

    list_of_traffic_pattern = {}

    '''count number of pathes between host couples'''
    for path in pathes:
        src_host_ip = path[0]
        dst_host_ip = path[-1]
        if (src_host_ip, dst_host_ip) not in path_detector:
            path_detector[(src_host_ip, dst_host_ip)] = 1
            list_of_traffic_pattern[src_host_ip] = []
        else:
            path_detector[(src_host_ip, dst_host_ip)] = path_detector[(src_host_ip, dst_host_ip)] + 1

    global helperIPAddress
    for j in range(0, len(pathes)):
        src_host_ip = pathes[j][0]
        dst_host_ip = pathes[j][-1]
        ip_protocol = "icmp"

        list_of_traffic_pattern[src_host_ip].append(
            {"dst_ip": helperIPAddress, "ip_tos": path_detector[(src_host_ip, dst_host_ip)],
             "ip_protocol": ip_protocol,
             "flow_label": j})
        path_detector[(src_host_ip, dst_host_ip)] = path_detector[(src_host_ip, dst_host_ip)] - 1

    global PG_manager_ip, PG_manager_port
    return __send_traffic_pattern_to_traffic_manager(list_of_traffic_pattern,PG_manager_ip,PG_manager_port), list_of_traffic_pattern, length

def _replace_dst_ip_with_helper_ip_address(path=None):
    """
    Replaces destination ip addresses to helper ip address
    :param path:
    :return:
    """
    if path is None:
        path = ['10.0.0.3', '00:00:00:00:00:00:00:1b', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:11',
                '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:13', '00:00:00:00:00:00:00:0b',
                '00:00:00:00:00:00:00:15', '00:00:00:00:00:00:00:1b', '10.0.0.3']
    path[-1] = helperIPAddress
    return path


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

def create_dir_recursively (dir):
    import pathlib
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

def get_file_names_in_a_directory(dir):
    import os
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files

def sort_list_of_tupples_by_nth_element(l,n):
    return sorted(l, key=lambda x: x[n])