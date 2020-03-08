from utilities import add_dic_to_file,delete_test_hosts_from_topo_matrix,ThreadWithReturnValue,generate_flows,get_test_hosts_traffic_pattern_from_link_info,convert_host_ip_to_sw_dpid,generate_flows_to_test_hosts,TopoInteractions,create_dir_recursively
import pprint
from modules.sdn_applications.floodlight.rest_client_for_floodlight import ControllerApi as FloodlightAPI
import utilities


from utilities import PG_manager_ip,PG_manager_port,PG_manager_port_test,controller_ip,controller_port,helperIPAddress,helperMACAddress


# PG_manager_ip = "10.0.0.202"
# PG_manager_port = 5000
# PG_manager_port_test = 5050

# controller_ip = "10.0.0.200"
# # controller_ip = "192.168.254.128"
# # controller_ip = "127.0.0.1"
# controller_port = 8080

# helperIPAddress = "10.0.0.250"
# helperMACAddress = "00:00:00:00:00:fa"

# ipToMACAddressMap = {}
# MACtoIPAddressMap = {}

# topo_links = {}
# pp = pprint.PrettyPrinter(depth=2)

# test_hosts_last_octet_is_greater_than = 100

def main():
    topo_interactions = TopoInteractions()

    '''
    Get topology from controller, by Hesam
    '''
    controller_api = FloodlightAPI(controller_ip,controller_port)
    # global ipToMACAddressMap, topo_links, MACtoIPAddressMap
    topo_neighbourhood_matrix,topo_interactions.topo_links,topo_interactions.ipToMACAddressMap,topo_interactions.MACtoIPAddressMap = controller_api.get_topo_from_controller()

    # global test_hosts_last_octet_is_greater_than
    topo_neighbourhood_matrix,contain_host = delete_test_hosts_from_topo_matrix(topo_neighbourhood_matrix,utilities.test_hosts_last_octet_is_greater_than)
    if not contain_host:
        print ("no host is detected, plz pingall in mininet")
        return 2

    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))

    from pathlib import Path

    base_output_path = Path(dir_path) / Path("evaluation") / Path("emulation") / Path("latest") / Path("outputs")
    create_dir_recursively (base_output_path)
    create_dir_recursively (base_output_path / Path("other"))
    print ("topo_neighbourhood_matrix: ",topo_neighbourhood_matrix)
    add_dic_to_file(topo_neighbourhood_matrix,base_output_path/"1.topology_matrix.txt")
    print ("topo_links: ",topo_interactions.topo_links)
    add_dic_to_file(topo_interactions.topo_links,base_output_path / Path("other") / "topo_links.txt")
    print ("ipToMACAddressMap: ",topo_interactions.ipToMACAddressMap)
    add_dic_to_file(topo_interactions.ipToMACAddressMap,base_output_path / Path("other") / "ip_to_mac_add_map.txt")
    print ("MACtoIPAddressMap: ",topo_interactions.MACtoIPAddressMap)
    add_dic_to_file(topo_interactions.MACtoIPAddressMap,base_output_path / Path("other") / "mac_to_ip_address_map.txt")

    ''' 
    Output of LP algorithm, by Mehdi
    '''
    from modules.path_and_flow_selector_heuristic_PSF import heuristic_for_ILP
    length_of_probes_array = [2, 5]
    topo = topo_neighbourhood_matrix
    node_based_path_array,_,_,_ = heuristic_for_ILP(topo=topo, length_of_probes_array=length_of_probes_array, debug=False)

    print ("node_based_path_array: ",node_based_path_array)
    
    pathes_path = base_output_path / "2.Pathes.txt"
    add_dic_to_file(node_based_path_array,pathes_path)


    # base_output_path = "../latest/outputs/"
    # pathes_path = base_output_path + "2.Pathes.txt"
    #
    # with open(pathes_path) as pathes_file:
    #     str_from_file = pathes_file.read().replace("\'","\"")
    #     pathes = json.loads(str_from_file)


    

    '''
    Push flow entries to switches, by Hesam
    '''
    ok,flows = topo_interactions.push_flows(node_based_path_array)
    if ok != True:
        print ("Error: Can't push flow entries.")
        return

    add_dic_to_file(flows,base_output_path / Path("other") / "rules.txt")

    
    '''
    Command Packet Traffic Manager to generate traffic in network, by Hesam
    '''

    # f= open("pathes_by_mahdi.txt","w+")
    #    f.write(json.dumps(pathes))
    # f.close()

#     end_to_end_delay_matrix, list_of_traffic_patterns, length = generate_flows(node_based_path_array)
#     end_to_end_delay_matrix_list = [{}] * length
# #    print ("length: ", length)
# #    print ("length result: ", len(end_to_end_delay_matrix_list))
#     for src_ip, l in end_to_end_delay_matrix.items():
#         # print src_ip, "=>", list
#         for flows in end_to_end_delay_matrix[src_ip]:
# #            print ("flows: ", flows)
#             # for i in range (0,len(flows)-1):
# #            print ('flows["flow_label"]: ', flows["flow_label"])
#             # print ('end_to_end_delay_matrix[src_ip]:',end_to_end_delay_matrix[src_ip])
#            # print (flows["flow_label"])
#             end_to_end_delay_matrix_list[flows["flow_label"]] = {src_ip: flows}
#
#     # print ("list_of_traffic_patterns: ",list_of_traffic_patterns )
#     add_dic_to_file(list_of_traffic_patterns,"../latest/outputs/other/list_of_traffic_patterns.txt")
#     add_dic_to_file(end_to_end_delay_matrix, "../latest/outputs/other/end_to_end_delay_matrix_dic.txt")
#     add_dic_to_file(end_to_end_delay_matrix_list, "../latest/outputs/3.end_to_end_delay_matrix.txt")




    """ test hosts traffic generation to calculate real link delays"""

    # end_to_end_delay_matrix, list_of_traffic_patterns, length = generate_flows(node_based_path_array)
    th1 =  ThreadWithReturnValue(target=generate_flows, args=(node_based_path_array,))

    # end_to_end_delay_matrix_test = generate_flows_to_test_hosts(get_test_hosts_traffic_pattern_from_link_info(topo_links))
    th2 = ThreadWithReturnValue(target=generate_flows_to_test_hosts,
                                args=(get_test_hosts_traffic_pattern_from_link_info(topo_interactions.topo_links),))
    th1.start()
    th2.start()

    print (" wait until thread 1 finishes")
    end_to_end_delay_matrix, list_of_traffic_patterns, length = th1.join()  # wait until thread 1 finishes
    print(" wait until thread 2 finishes")
    end_to_end_delay_matrix_test, _ = th2.join() #wait until thread 2 finishes



    #end_to_end_delay_matrix, list_of_traffic_patterns, length = generate_flows(node_based_path_array)
    end_to_end_delay_matrix_list = [{}] * length
    #    print ("length: ", length)
    #    print ("length result: ", len(end_to_end_delay_matrix_list))
    for src_ip, l in end_to_end_delay_matrix.items():
        # print src_ip, "=>", list
        for flows in end_to_end_delay_matrix[src_ip]:
            #            print ("flows: ", flows)
            # for i in range (0,len(flows)-1):
            #            print ('flows["flow_label"]: ', flows["flow_label"])
            # print ('end_to_end_delay_matrix[src_ip]:',end_to_end_delay_matrix[src_ip])
            # print (flows["flow_label"])
            end_to_end_delay_matrix_list[flows["flow_label"]] = {src_ip: flows}

    # print ("list_of_traffic_patterns: ",list_of_traffic_patterns )
    add_dic_to_file(list_of_traffic_patterns, base_output_path / Path("other") / "list_of_traffic_patterns.txt")
    add_dic_to_file(end_to_end_delay_matrix, base_output_path / Path("other") / "end_to_end_delay_matrix_dic.txt")
    add_dic_to_file(end_to_end_delay_matrix_list, base_output_path / "3.TGM_end_to_end_delay_matrix.txt")

    add_dic_to_file(end_to_end_delay_matrix_test, base_output_path / Path("other") /"end_to_end_delay_matrix_dic_test.txt")

    '''
    PSO Part
    '''
    from modules.delay_matrix_calculator_DMC_PSO import PSO,link_delay_measurement_PSO,link_delay_measurement_and_comparison_PSO


    #real_link_delays = {('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:0b'): 3}

    ###### actual delay ##########
#    base_output_path = "../latest/outputs/"
#    actual_link_delay_path = base_output_path + "actual_link_delay_matrix.txt"
    #with open(actual_link_delay_path) as actual_link_delay_file:
##        str_from_file = actual_link_delay_file.read().replace("\'","\"")
#        actual_link_delay = json.loads(str_from_file)


    # real_link_delays={}
    # for k, v in actual_link_delay.items():
    #     real_link_delays[(__convert_to_colon_separated(k.split("|")[0]), __convert_to_colon_separated(k.split("|")[1]))] = v

    real_link_delays = {}

    for src in end_to_end_delay_matrix_test:
        for item in end_to_end_delay_matrix_test[src]:
            dst = item['match']['dst_ip']
            src_dpid = convert_host_ip_to_sw_dpid(src)
            dst_dpid = convert_host_ip_to_sw_dpid(dst)
            real_link_delays[(src_dpid, dst_dpid)] = item['min'] / 2

    print("real_link_delays: ")
    print (real_link_delays)
    #node_based_path_array = []
    ###### actual delay ##########


    ########delay array###########
    #base_output_path = "./latest/outputs/"
    end_to_end_delay_file_path = base_output_path/"3.TGM_end_to_end_delay_matrix.txt"
    array_of_delays = []
    with open(end_to_end_delay_file_path) as end_to_end_delay_file:
        str_from_file = end_to_end_delay_file.read().replace("\'", "\"")
        l = json.loads(str_from_file)

    min=[]
    for item in l:
        for i in item.values():
            min.append(i["min"])

    array_of_delays = min
    ########delay array###########

    print (array_of_delays)
    print (node_based_path_array)
    print (real_link_delays)
    create_dir_recursively (base_output_path / Path("DMI"))

    add_dic_to_file(array_of_delays, base_output_path / Path("DMI") / "pso_array_of_delays.txt")
    add_dic_to_file(node_based_path_array, base_output_path / Path("DMI") / "pso_node_based_path_array.txt")
    add_dic_to_file(real_link_delays, base_output_path / Path("other") /"real_link_delays_by_test_hosts.txt")
    
    
    measured_link_delay = link_delay_measurement_PSO(array_of_delays, node_based_path_array, debug=False)

    #add_dic_to_file (measured_link_delay, base_output_path / Path("other") / "4.DMI_measured_link_delay.txt")
    add_dic_to_file (measured_link_delay, base_output_path / Path("DMI") / "measured_link_delay.txt")

    # print("Max error per one link: ", max_difference)
    # print('Summation of all link delays error: ', link_delay_error)

    max_difference, link_delay_error= link_delay_measurement_and_comparison_PSO(array_of_delays, node_based_path_array, real_link_delays, debug=False,save_to_file_dir= base_output_path / "4.DMI_measured_link_delay.txt")

    add_dic_to_file (max_difference, base_output_path / Path("DMI") / "max difference.txt")
    add_dic_to_file (link_delay_error, base_output_path / Path("DMI") / "link delay error.txt" )
    

#    actual_res = []
#    j = 0
#    for path in node_based_path_array:
#        j = j + 1

#        delay = 0
#        for i in range(1, len(path) - 2):
            # print (path[i].replace(":","")+"|"+path[i+1].replace(":",""))
            # print (actual[path[i].replace(":","")+"|"+path[i+1].replace(":","")])
#            delay = delay + actual_link_delay[path[i].replace(":", "") + "|" + path[i + 1].replace(":", "")]
#        actual_res.append(delay)

    #print ("actual_link_delay: "+str(actual_res))




    '''
    Call Packet Generators API's one by one, by Hesam
    '''
    #    end_to_end_delay_matrix = call_packet_generator_manager_api(list_of_packet_generator_and_their_tasks)

    # end_to_end_delay_matrix = {"'10.0.0.1'": [{"average": 2.9840000000000004, "detailed_rtt": [3.6, 3.3, 3.0, 2.0, 1.1, 4.0, 3.1, 2.2, 1.3, 0.4, 4.5, 3.9, 2.9, 2.0, 1.1, 3.7, 2.9, 2.7, 2.5, 1.9, 1.2, 4.6, 3.7, 2.8, 2.0, 1.1, 3.7, 2.8, 1.9, 1.0, 3.7, 2.8, 1.9, 1.0, 4.6, 3.7, 2.8, 1.9, 1.0, 3.8, 2.8, 1.8, 1.0, 8.2, 7.4, 6.5, 5.7, 4.8, 3.9, 3.0], "match": {"dst_ip": "'10.0.0.3'", "ip_protocol": "icmp", "ip_tos": "1"}, "max": 8.2, "min": 0.4}, {"average": 3.328000000000001, "detailed_rtt": [3.7, 3.0, 1.9, 1.0, 0.1, 3.7, 2.9, 1.9, 1.0, 3.8, 2.9, 2.0, 1.1, 8.3, 7.5, 7.4, 6.5, 5.6, 4.7, 3.8, 2.9, 1.9, 0.9, 3.7, 2.9, 2.0, 1.0, 4.7, 3.8, 2.9, 1.9, 1.2, 3.7, 2.9, 1.8, 1.0, 3.7, 2.8, 1.9, 1.0, 8.3, 7.3, 6.4, 5.6, 4.5, 3.7, 2.7, 1.9, 0.8, 3.8], "match": {"dst_ip": "'10.0.0.3'", "ip_protocol": "icmp", "ip_tos": "1"}, "max": 8.3, "min": 0.1}]}

    '''
    Genetic Algorithm is waiting for Packet Generator Results, by Mehdi
    '''

    # link_delay_list = genetic_algorith(end_to_end_delay_matrix)
    # sample output

    link_delay_list = '''

    {('00:00:00:00:00:00:00:01','s1-eth2', '00:00:00:00:00:00:00:02',s2-eth3, 's'): 1.32,

    ('00:00:00:00:00:00:00:02','s2-eth2', '00:00:00:00:00:00:00:03',s2-eth1, 's'): 1.02,

    ('10.0.0.1','h1-eth0', '00:00:00:00:00:00:00:01',s1-eth1, 'h'): 0.021,

    ('10.0.0.2','h2-eth0', '00:00:00:00:00:00:00:02',s2-eth1, 'h'): 0.022,

    ('10.0.0.3','h3-eth0', '00:00:00:00:00:00:00:03',s3-eth1, 'h'): 0.012

    }

    '''


if __name__ == '__main__':
    import logging

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    import json
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='This script is for running coordinator on desired host. This components make connection with controller to get topology and then use BLP algorithm to calculate pathes. Then tries to push flow entries using controller REST API. Now it\'s time to command traffic manager to generate traffic on traffic agents and get rtt info from traffic manager. By using a genetic algorithm, coordinator simpley can calcuate links delays of topology.')
    # parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
    # parser.add_argument('--port', dest='port', help="Listen port for traffic manager REST API.")

    args = parser.parse_args()
    # config_file_path             = args.config_file_path
    # listen_port                  = args.port

    # if config_file_path != None:
    # with open(config_file_path) as config_file:
    # data = json.load(config_file)

    main()
