from utilities import add_dic_to_file,delete_test_hosts_from_topo_matrix,ThreadWithReturnValue,generate_flows,get_test_hosts_traffic_pattern_from_link_info,convert_host_ip_to_sw_dpid,generate_flows_to_test_hosts,TopoInteractions,create_dir_recursively,get_file_names_in_a_directory,sort_list_of_tupples_by_nth_element
import pprint
from modules.sdn_applications.floodlight.rest_client_for_floodlight import ControllerApi as FloodlightAPI
import utilities


from utilities import PG_manager_ip,PG_manager_port,PG_manager_port_test,controller_ip,controller_port,helperIPAddress,helperMACAddress

length_of_probes_array = []
NUMBER_OF_HOSTS = None

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

def parse_flags():
    import argparse
    parser = argparse.ArgumentParser(
        description='This script is for running coordinator on desired host. This components make connection with controller to get topology and then use BLP algorithm to calculate pathes. Then tries to push flow entries using controller REST API. Now it\'s time to command traffic manager to generate traffic on traffic agents and get rtt info from traffic manager. By using a genetic algorithm, coordinator simpley can calcuate links delays of topology.')
    # parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
    # parser.add_argument('--port', dest='port', help="Listen port for traffic manager REST API.")
    parser.add_argument('-l','--length_of_probes_array', nargs='+', help='<Required> Sets len of probes array for example:\n\t program.py -l 2 5', dest='length_of_probes_array',type=int, required=False)
    parser.add_argument('--debug', dest='debug', help="Print debug outputs.",action="store_true")
    parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. abilene",required=True,type=str)
    parser.add_argument('--n', dest='number_of_hosts', help="Number of hosts in topology",required=False,type=int)
    parser.add_argument('--new', dest='dont_continue_from_last_run', help="If you wanna save the results in similar path with last run and merge some csv files, don't use this flag",required=False,action="store_true",default=False)

    global length_of_probes_array,debug,TOPOLOGY_NAME,NUMBER_OF_HOSTS,args
    args = parser.parse_args()

    length_of_probes_array = args.length_of_probes_array
    debug = args.debug

    TOPOLOGY_NAME = args.topo_name#"abilene"
    NUMBER_OF_HOSTS = args.number_of_hosts#2

def get_all_subset(lst):
    import itertools 
    a1= [list(itertools.combinations(lst, i+1)) for i in range(len(lst))]
    return [x for y in a1 for x in y]

def get_sequential_subsets(lst,min_len=1):
    """
    param lst, e.g. : [1,2,3,4,5,6,7,8]

    return [[1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8]]
    """
    return [lst[0:i] for i in range(min_len,len(lst)+1)]


def main():
    import logging,json,sys,os
    import csv
    from pathlib import Path
    from datetime import date,datetime
    global NUMBER_OF_HOSTS


    format = "[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logger= logging.getLogger()

    parse_flags()

    module_path = Path(os.path.dirname(os.path.realpath(__file__)))
    #create directory for saving results

    #current_path = Path.cwd()  #current dir
    #module_path = Path(__file__).parent


    '''
    Get topology from controller, by Hesam
    '''
    topo_interactions = TopoInteractions()
    controller_api = FloodlightAPI(controller_ip,controller_port)
    
    #clear all flows from last executions if exists
    controller_api.del_flows()

    topo_neighbourhood_matrix,topo_interactions.topo_links,topo_interactions.ipToMACAddressMap,topo_interactions.MACtoIPAddressMap = controller_api.get_topo_from_controller()

    topo_neighbourhood_matrix,contain_host = delete_test_hosts_from_topo_matrix(topo_neighbourhood_matrix,utilities.test_hosts_last_octet_is_greater_than)
    if not contain_host:
        logger.info("no host is detected, plz pingall in mininet")
        exit(2)
    

    hosts = set()
    for item in topo_neighbourhood_matrix:
        if item[2]=='h':
            hosts.add(item[0])
    
    global NUMBER_OF_HOSTS
    if NUMBER_OF_HOSTS is not len(hosts) and NUMBER_OF_HOSTS is not  None:
        print("topology doesn't have your number of hosts specified using --n\n number_of_hosts is: {}".format(len(hosts)))
        exit(1)
    
    #NUMBER_OF_HOSTS = len (hosts)
    
    

    
    
    date = date.today() #2020-02-19
    time = datetime.now().strftime("%I:%M%p") #04:12PM

    global TOPOLOGY_NAME ,args
    base_output_path = Path(module_path) / "evaluation" / "emulation" / "latest" / "outputs_{}_{}".format(date,time) 


    ##if wanna continue from last run, we have to load last run path
    history_file_path =  module_path / ".history"
    last_run_output_path = None

    # if os.path.isdir(history_file_path):
    f = None
    try:
        f = open (history_file_path,"r+")
    except IOError:
        f = open (history_file_path,"w+")

    try:
        data = f.read()
        data = data.split("\n")
        last_run_output_path = data[-1]
        if not args.dont_continue_from_last_run:
            if len(data) is 0 or last_run_output_path is "":
                print ("Cannot continue because this is first run, please use --new flag.")
                exit(1)
            
        # #f.seek(0)
        # if len(data) is 0:
        #     f.write(str(base_output_path)) #save last run dir
        # elif data[-1] is "":
        #     f.write(str(base_output_path)) #save last run dir
        # else:
        #     f.write("\n"+str(base_output_path)) #save last run dir
        #f.truncate()
    except Exception as e:
        logger.info(e) 
        exit(2)
    
    f.close()


    if not args.dont_continue_from_last_run:
        if last_run_output_path is not None:
            base_output_path = Path(last_run_output_path)
        else:
            print ("Something wrong happened, you cannot continue, sorry!")

    emulation_results_dir = base_output_path / "{}_{}".format(TOPOLOGY_NAME,str(NUMBER_OF_HOSTS))
    print (emulation_results_dir)
    debug_dir = emulation_results_dir / Path("debug")  
    isdir = os.path.isdir(emulation_results_dir)

    if isdir:
        warning_text = None
        if not args.dont_continue_from_last_run:
            warning_text = "You ran for this number of hosts earlier. You can use --new flag or please confirm that you want to overwrite it without new run? y/n\n"
        else:
            warning_text = "Same directory for you output is avaiable \"{}\", You can use --new flag or please confirm that you want to overwrite it without new run? y/n\n".format(base_output_path)
        for i in range(3):
            yes_or_no = input(warning_text)
            if yes_or_no.lower()=='n' or i is 2:
                exit(1)
            elif yes_or_no.lower()=='y':
                import shutil
                shutil.rmtree(base_output_path)
                break


    f = None
    try:
        f = open (history_file_path,"r+")
    except IOError:
        f = open (history_file_path,"w+")

    try:
        data = f.read()
        data = data.split("\n")
        last_run_output_path = data[-1]
            
        #f.seek(0)
        if len(data) is 0:
            f.write(str(base_output_path)) #save last run dir
        elif last_run_output_path is "":
            f.write(str(base_output_path)) #save last run dir
        else:
            f.write("\n"+str(base_output_path)) #save last run dir
        #f.truncate()
    except Exception as e:
        logger.info(e) 
        exit(2)
    
    f.close()


    create_dir_recursively (debug_dir)
    create_dir_recursively (base_output_path)
    # charts_data_dir = base_output_path / Path("charts_data")
    # create_dir_recursively(charts_data_dir)

    ##csv outputs##
    evaluation_csv_path_all = base_output_path / "csv" / "all_{}_{}.csv".format(TOPOLOGY_NAME,str(NUMBER_OF_HOSTS))
    evaluation_csv_path_solved = base_output_path / "csv" / "solved_{}_{}.csv".format(TOPOLOGY_NAME,str(NUMBER_OF_HOSTS))
    evaluation_csv_path_barchart_bar_min_length_of_routes_with_different_monitoring_nodes = base_output_path / "csv" / "barchart_bar_min_length_of_routes_with_different_monitoring_nodes.csv"
    evaluation_csv_path_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved = base_output_path / "csv" / "barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.csv"
    evaluation_csv_path_barchart_summation_of_all_links_delay_max_len_of_route_all_solved = base_output_path / "csv" / "barchart_summation_of_all_links_delay_max_len_of_route_all_solved.csv"
    evaluation_csv_path_barchart_max_link_delay_error_max_len_of_route_all_solved = base_output_path / "csv" / "barchart_max_link_delay_error_max_len_of_route_all_solved.csv"
    evaluation_csv_path_barchart_real_and_measured_delay_max_len_of_route_all_solved = base_output_path / "csv" /  "{}_{}_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv".format(TOPOLOGY_NAME,str(NUMBER_OF_HOSTS))

    


    create_dir_recursively (base_output_path / "csv")
    



    

    ###configs###
    max_hop_count_path = 15
    SEQUENTIAL_LEN_OF_PROBE_ARRAYS = True
    #TOPOLOGY_EXCLUDE = ["Geant"]
    TOPOLOGY_EXCLUDE = [" "]
    DURATION_RUN_LIMIT_MS = 0

    min_max_length_of_routes_all_topologies_solved = 11 #this number is for abilene topology#
    #TOPOLOGY_NAME = "abilene"
    #NUMBER_OF_HOSTS = 2




    
    
    with open(evaluation_csv_path_all, 'a', newline='') as csv_file_results_all,\
        open(evaluation_csv_path_solved, 'a', newline='') as csv_file_results_solved,\
        open(evaluation_csv_path_barchart_bar_min_length_of_routes_with_different_monitoring_nodes, 'a', newline='') as csv_file_barchart_bar_min_length_of_routes_with_different_monitoring_nodes,\
        open(evaluation_csv_path_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_summation_of_all_links_delay_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_summation_of_all_links_delay_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_max_link_delay_error_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_max_link_delay_error_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_real_and_measured_delay_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_real_and_measured_delay_max_len_of_route_all_solved:
        


        
        csv_writer_results_all = csv.writer(csv_file_results_all,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)
    
        csv_writer_results_solved = csv.writer(csv_file_results_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)
        
        csv_writer_barchart_bar_min_length_of_routes_with_different_monitoring_nodes = csv.writer(csv_file_barchart_bar_min_length_of_routes_with_different_monitoring_nodes,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved = csv.writer(csv_file_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved = csv.writer(csv_file_barchart_summation_of_all_links_delay_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved = csv.writer(csv_file_barchart_max_link_delay_error_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved = csv.writer(csv_file_barchart_real_and_measured_delay_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)


        csv_writer_results_all.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#max_len_of_probes_array","#number_of_existing_links","#number_of_switches","#percent_of_hosts","#links_monitored_percent","#number_of_hosts","#number_of_rules","#number_of_flows","max_error_per_one_link", "#summation_of_all_link_delays_error","#run_duration_ms_pso"])

        csv_writer_results_solved.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#max_len_of_probes_array","#number_of_existing_links","#number_of_switches","#percent_of_hosts","#links_monitored_percent","#number_of_hosts","#number_of_rules","#number_of_flows","max_error_per_one_link", "#summation_of_all_link_delays_error","#run_duration_ms_pso"])

        csv_writer_barchart_bar_min_length_of_routes_with_different_monitoring_nodes.writerow(["#number_of_hosts","#min_length_of_routes_with_different_monitoring_nodes"])

        csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.writerow(["#number_of_hosts","#average_rules","###min_max_length_of_probes_array_all_sovled = {}".format(min_max_length_of_routes_all_topologies_solved)])

        csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved.writerow(["#number_of_hosts","#summation_of_all_links_delay_max_len_of_route_all_solved","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])

        csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved.writerow(["#number_of_hosts","#max_link_delay_error_max_len_of_route_all_solved","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])


        csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved.writerow(["#number_of_hosts","#real_delay","#measured_delay","#link_id","#link_name","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])
        
        
        if debug: logger.info("topo_neighbourhood_matrix: {}".format(topo_neighbourhood_matrix))
        add_dic_to_file(topo_neighbourhood_matrix,emulation_results_dir / "1.topology_matrix.txt")
        if debug: logger.info("topo_links: {}".format(topo_interactions.topo_links))
        add_dic_to_file(topo_interactions.topo_links,debug_dir / "topo_links.txt")
        if debug: logger.info("ipToMACAddressMap: {}".format(topo_interactions.ipToMACAddressMap))
        add_dic_to_file(topo_interactions.ipToMACAddressMap,debug_dir / "ip_to_mac_add_map.txt")
        if debug: logger.info("MACtoIPAddressMap: {}".format(topo_interactions.MACtoIPAddressMap))
        add_dic_to_file(topo_interactions.MACtoIPAddressMap,debug_dir / "mac_to_ip_address_map.txt")

        
        initial_length_of_probes_array = range(2,3)
        from modules.path_and_flow_selector_heuristic_PSF import heuristic_for_ILP
        nodeBasedPath_arrayOfList,number_of_probes,number_of_existing_links,number_of_included_links = heuristic_for_ILP(topo=topo_neighbourhood_matrix, length_of_probes_array=initial_length_of_probes_array, debug=False)

        switches = set()
        for item in topo_neighbourhood_matrix:
            if item[2]=='s':
                switches.add(item[0])
        number_of_switches = len (switches)

        percent_of_hosts = int (100.0 * NUMBER_OF_HOSTS / number_of_switches)

        all_sets = None
        path_length_array = range(2,max_hop_count_path+1)    
        if SEQUENTIAL_LEN_OF_PROBE_ARRAYS:
            all_sets = get_sequential_subsets(path_length_array)
        else:
            all_sets = get_all_subset(path_length_array)

        global length_of_probes_array
        if length_of_probes_array is not None:
            all_sets = []
            all_sets.append(length_of_probes_array)


        #initialize widgets
        import progressbar as pb
        widgets = ['topo: {}, hosts: {}, switches: {}, links: {} --> '.format(TOPOLOGY_NAME,NUMBER_OF_HOSTS,number_of_switches,number_of_existing_links), pb.Percentage(), ' ', 
        pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]


        #initialize timer
        timer = pb.ProgressBar(widgets=widgets, maxval=len(all_sets)).start()

        #length_of_probes_array = []
        link_monitored_percent_reached_to_100 = False
        i=0
        for length_of_probes_array in all_sets:
            print ("\n\n\t\t*******")
            number_of_probes = number_of_included_links = run_duration_ms_ilp=max_len_of_probes_array=number_of_existing_links=links_monitored_percent=number_of_rules=number_of_flows= max_error_per_one_link= summation_of_all_link_delays_error=run_duration_ms_pso = 0


            max_len_of_probes_array = max(length_of_probes_array)
            import time
            start_time = time.time()
            ''' 
            Output of ILP algorithm, by Mehdi
            '''
            #length_of_probes_array = [2, 5]
            #global length_of_probes_array
            topo = topo_neighbourhood_matrix
            import time
            start_time = time.time()
            node_based_path_array,number_of_flows,number_of_existing_links,number_of_included_links = heuristic_for_ILP(topo=topo, length_of_probes_array=length_of_probes_array, debug=debug)
            end_time = time.time()
            run_duration_ms_ilp = round((end_time-start_time)*1000,3)

            logger.info("ILP Algorithm (PSF Module) run duration: {}ms\n".format(run_duration_ms_ilp))
            links_monitored_percent = round(number_of_included_links*1.0/number_of_existing_links,2)*100

            
            logger.info("percent of links monitored: {}.\n max length of probes array: {}".format(links_monitored_percent,max_len_of_probes_array))
            if links_monitored_percent < 100:
                csv_writer_results_all.writerow([number_of_probes,number_of_included_links,run_duration_ms_ilp,max_len_of_probes_array,number_of_existing_links,number_of_switches,percent_of_hosts,links_monitored_percent,NUMBER_OF_HOSTS,number_of_rules,number_of_flows, round(max_error_per_one_link,2), round(summation_of_all_link_delays_error,2),run_duration_ms_pso])

                #exit(1)
                i = i+1 
                timer.update(i)
                continue


            if not link_monitored_percent_reached_to_100 and int(links_monitored_percent) is 100:
                csv_writer_barchart_bar_min_length_of_routes_with_different_monitoring_nodes.writerow([NUMBER_OF_HOSTS,max_len_of_probes_array])
                link_monitored_percent_reached_to_100 = True

            if debug: logger.info("node_based_path_array: {}".format(node_based_path_array))



            pathes_path = emulation_results_dir / "2.Pathes.txt"
            add_dic_to_file(node_based_path_array,pathes_path)

 
            '''
            Push flow entries to switches, by Hesam
            '''
            logger.info("Clearing switch flow entries.")
            controller_api.del_flows()
            logger.info("Pushing flow entries for {} pathes".format(len(node_based_path_array)))
            ok,rules = topo_interactions.push_flows(node_based_path_array,debug=debug)
            if ok != True:
                logger.info("Error: Can't push flow entries.")
                continue
            logger.info("{} flow entries added\n".format(len(rules)))
            add_dic_to_file(number_of_flows,emulation_results_dir / "number_of_needed_flows.txt")

            add_dic_to_file(rules,debug_dir / "rules.txt")
            number_of_rules = len(rules)
   

            add_dic_to_file(number_of_rules,emulation_results_dir / "number_of_needed_rules.txt")
            
            logger.info("Number of flows: {}".format(number_of_flows))
            logger.info("Number of flows: {}".format(number_of_rules))

            
            '''
            Command Packet Traffic Manager to generate traffic in network, by Hesam
            '''
            th1 =  ThreadWithReturnValue(target=generate_flows, args=(node_based_path_array,))
            th2 = ThreadWithReturnValue(target=generate_flows_to_test_hosts,
                                        args=(get_test_hosts_traffic_pattern_from_link_info(topo_interactions.topo_links),))
            th1.start()
            logger.info("Generating flows through TMA Instances")
            th2.start()
            logger.info("Generating flows through test TMA Instances")

            logger.info("Waiting for TGA instances to finish...")
            end_to_end_delay_matrix, list_of_traffic_patterns, length = th1.join()  # wait until thread 1 finishes

            if len(end_to_end_delay_matrix) == 0 :
                logger.error("Some trouble happened in TGM Instance, please check it.")
                exit(0)
            logger.info("Waiting for TGA test instances to finish")
            end_to_end_delay_matrix_test, _ = th2.join() #wait until thread 2 finishes


            end_to_end_delay_matrix_list = [{}] * length

            for src_ip, l in end_to_end_delay_matrix.items():
                for flows in end_to_end_delay_matrix[src_ip]:
                    end_to_end_delay_matrix_list[flows["flow_label"]] = {src_ip: flows}

            add_dic_to_file(list_of_traffic_patterns, debug_dir / "list_of_traffic_patterns.txt")
            add_dic_to_file(end_to_end_delay_matrix, debug_dir / "end_to_end_delay_matrix_dic.txt")
            add_dic_to_file(end_to_end_delay_matrix_list, emulation_results_dir / "3.TGM_end_to_end_delay_matrix.txt")

            add_dic_to_file(end_to_end_delay_matrix_test, debug_dir /"end_to_end_delay_matrix_dic_test.txt")


            '''
            Calculating array of delays, input of PSO Algorithm
            '''
            real_link_delays = {}

            for src in end_to_end_delay_matrix_test:
                for item in end_to_end_delay_matrix_test[src]:
                    dst = item['match']['dst_ip']
                    src_dpid = convert_host_ip_to_sw_dpid(src)
                    dst_dpid = convert_host_ip_to_sw_dpid(dst)
                    real_link_delays[(src_dpid, dst_dpid)] = item['min'] / 2

            if debug: logger.info("real_link_delays: {}".format(real_link_delays))
            

            min=[]
            for item in end_to_end_delay_matrix_list:
                for it in item.values():
                    min.append(it["min"])

            array_of_delays = min

            ###save outputs to file###
            create_dir_recursively (emulation_results_dir / Path("DMI"))
            add_dic_to_file(array_of_delays, emulation_results_dir / Path("DMI") / "pso_array_of_delays.txt")
            add_dic_to_file(node_based_path_array, emulation_results_dir / Path("DMI") / "pso_node_based_path_array.txt")
            add_dic_to_file(real_link_delays, debug_dir /"real_link_delays_by_test_hosts.txt")
            
            
            '''
            PSO Algorithm
            '''
            from modules.delay_matrix_calculator_DMC_PSO import PSO,link_delay_measurement_PSO,link_delay_measurement_and_comparison_PSO

            start_time = time.time()
            measured_link_delay = link_delay_measurement_PSO(array_of_delays, node_based_path_array, debug=debug)
            end_time = time.time()
            run_duration_ms_pso = round((end_time-start_time)*1000,3)
            logger.info("PSO Algorithm (DMI Module) run duration: {}ms\n".format(run_duration_ms_pso))



            ###save all results###
            add_dic_to_file (measured_link_delay, emulation_results_dir / Path("DMI") / "measured_link_delay.txt")


            max_error_per_one_link, summation_of_all_link_delays_error,link_real_and_measured_delay= link_delay_measurement_and_comparison_PSO(array_of_delays, node_based_path_array, real_link_delays, debug=debug,save_to_file_dir= emulation_results_dir / "4.DMI_measured_link_delay.txt")

            ###writing DMI Module(PSO Algorithm) results into file
            add_dic_to_file (max_error_per_one_link, emulation_results_dir / Path("DMI") / "max_error_per_one_link.txt")
            add_dic_to_file (summation_of_all_link_delays_error, emulation_results_dir / Path("DMI") / "summation_of_all_link_delays_error.txt" )

            
            csv_writer_results_all.writerow([number_of_probes,number_of_included_links,run_duration_ms_ilp,max_len_of_probes_array,number_of_existing_links,number_of_switches,percent_of_hosts,links_monitored_percent,NUMBER_OF_HOSTS,number_of_rules,number_of_flows, round(max_error_per_one_link,2), round(summation_of_all_link_delays_error,2),run_duration_ms_pso])
            
            csv_writer_results_solved.writerow([number_of_probes,number_of_included_links,run_duration_ms_ilp,max_len_of_probes_array,number_of_existing_links,number_of_switches,percent_of_hosts,links_monitored_percent,NUMBER_OF_HOSTS,number_of_rules,number_of_flows, round(max_error_per_one_link,2), round(summation_of_all_link_delays_error,2),run_duration_ms_pso])

            if max_len_of_probes_array is min_max_length_of_routes_all_topologies_solved:
                csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,number_of_rules])
                csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,summation_of_all_link_delays_error])
                csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,max_error_per_one_link])

                link_id = 1
                for item in sort_list_of_tupples_by_nth_element(link_real_and_measured_delay,0):
                    link_name = item[0]
                    real_delay = item[1]
                    estimated_delay = item[2]
                    csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,real_delay,estimated_delay,link_id,'\"'+str(link_name)+'\"'])
                    link_id = link_id + 1

            i = i+1 
            timer.update(i)
        

if __name__ == '__main__':
    main()
