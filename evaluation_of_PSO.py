from pathlib import Path
import csv,logging
from datetime import date,datetime
import os
from utilities import add_dic_to_file,create_dir_recursively,sort_list_of_tupples_by_nth_element

format = "[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")
logger= logging.getLogger()

def parse_flags():
    import argparse
    parser = argparse.ArgumentParser(
        description='This script is for running coordinator on desired host. This components make connection with controller to get topology and then use BLP algorithm to calculate pathes. Then tries to push flow entries using controller REST API. Now it\'s time to command traffic manager to generate traffic on traffic agents and get rtt info from traffic manager. By using a genetic algorithm, coordinator simpley can calcuate links delays of topology.')
    # parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
    # parser.add_argument('--port', dest='port', help="Listen port for traffic manager REST API.")
   # parser.add_argument('-l','--length_of_probes_array', nargs='+', help='<Required> Sets len of probes array for example:\n\t program.py -l 2 5', dest='length_of_probes_array',type=int, required=False)
    parser.add_argument('--debug', dest='debug', help="Print debug outputs.",action="store_true")
    parser.add_argument('--toponame', dest='topo_name', help="Topology name e.g. abilene",required=True,type=str)
    parser.add_argument('--n', dest='number_of_hosts', help="Number of hosts in topology",required=False,type=int)
    #parser.add_argument('--new', dest='dont_continue_from_last_run', help="If you wanna save the results in similar path with last run and merge some csv files, don't use this flag",required=False,action="store_true",default=False)

    global length_of_probes_array,debug,TOPOLOGY_NAME,NUMBER_OF_HOSTS,args
    args = parser.parse_args()

   # length_of_probes_array = args.length_of_probes_array
    debug = args.debug

    TOPOLOGY_NAME = args.topo_name#"abilene"
    NUMBER_OF_HOSTS = args.number_of_hosts#2


parse_flags()
module_path = Path(os.path.dirname(os.path.realpath(__file__)))

global TOPOLOGY_NAME, NUMBER_OF_HOSTS
date = date.today() #2020-02-19
time = datetime.now().strftime("%I:%M%p") #04:12PM
base_output_path = Path(module_path) / "evaluation" / "emulation" / "latest" / "outputs_{}_{}".format(date,time) 
emulation_results_dir = base_output_path / "{}_{}".format(TOPOLOGY_NAME,str(NUMBER_OF_HOSTS))
min_max_length_of_routes_all_topologies_solved = 11 #this number is for abilene topology#


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
evaluation_csv_path_absolute_error_max_len_of_route_all_solved = base_output_path / "csv" / "absolute_error_max_len_of_route_all_solved.csv"

create_dir_recursively (base_output_path / "csv")


with open(evaluation_csv_path_all, 'a', newline='') as csv_file_results_all,\
        open(evaluation_csv_path_solved, 'a', newline='') as csv_file_results_solved,\
        open(evaluation_csv_path_barchart_bar_min_length_of_routes_with_different_monitoring_nodes, 'a', newline='') as csv_file_barchart_bar_min_length_of_routes_with_different_monitoring_nodes,\
        open(evaluation_csv_path_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_summation_of_all_links_delay_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_summation_of_all_links_delay_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_max_link_delay_error_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_max_link_delay_error_max_len_of_route_all_solved,\
        open(evaluation_csv_path_barchart_real_and_measured_delay_max_len_of_route_all_solved, 'a', newline='') as csv_file_barchart_real_and_measured_delay_max_len_of_route_all_solved,\
        open(evaluation_csv_path_absolute_error_max_len_of_route_all_solved, 'a', newline='') as csv_file_absolute_error_max_len_of_route_all_solved:
        


        
        csv_writer_results_all = csv.writer(csv_file_results_all,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)
    
        csv_writer_results_solved = csv.writer(csv_file_results_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)
        
        csv_writer_barchart_bar_min_length_of_routes_with_different_monitoring_nodes = csv.writer(csv_file_barchart_bar_min_length_of_routes_with_different_monitoring_nodes,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved = csv.writer(csv_file_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved = csv.writer(csv_file_barchart_summation_of_all_links_delay_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved = csv.writer(csv_file_barchart_max_link_delay_error_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved = csv.writer(csv_file_barchart_real_and_measured_delay_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_absolute_error_max_len_of_route_all_solved = csv.writer(csv_file_absolute_error_max_len_of_route_all_solved,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)


        csv_writer_results_all.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#max_len_of_probes_array","#number_of_existing_links","#number_of_switches","#percent_of_hosts","#links_monitored_percent","#number_of_hosts","#number_of_rules","#number_of_flows","max_error_per_one_link", "#summation_of_all_link_delays_error","#run_duration_ms_pso"])

        csv_writer_results_solved.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#max_len_of_probes_array","#number_of_existing_links","#number_of_switches","#percent_of_hosts","#links_monitored_percent","#number_of_hosts","#number_of_rules","#number_of_flows","max_error_per_one_link", "#summation_of_all_link_delays_error","#run_duration_ms_pso"])

        csv_writer_barchart_bar_min_length_of_routes_with_different_monitoring_nodes.writerow(["#number_of_hosts","#min_length_of_routes_with_different_monitoring_nodes"])

        csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.writerow(["#number_of_hosts","#average_rules","###min_max_length_of_probes_array_all_sovled = {}".format(min_max_length_of_routes_all_topologies_solved)])

        csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved.writerow(["#number_of_hosts","#summation_of_all_links_delay_max_len_of_route_all_solved","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])

        csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved.writerow(["#number_of_hosts","#max_link_delay_error_max_len_of_route_all_solved","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])

        csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved.writerow(["#number_of_hosts","#real_delay","#measured_delay","#link_id","#link_name","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])

        
        csv_writer_absolute_error_max_len_of_route_all_solved.writerow(["#number_of_hosts","absolute_error","###min_max_length_of_routes_all_topologies_solved = {}".format(min_max_length_of_routes_all_topologies_solved)])


        '''
        PSO Algorithm
        '''
        from modules.delay_matrix_calculator_DMC_PSO import PSO,link_delay_measurement_PSO,link_delay_measurement_and_comparison_PSO

        node_based_path_array = [['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.1', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', '10.0.0.1'], ['10.0.0.4', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '10.0.0.4'], ['10.0.0.4', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '10.0.0.4'], ['10.0.0.4', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', '10.0.0.4'], ['10.0.0.5', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', '10.0.0.5'], ['10.0.0.5', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', '10.0.0.5'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.4', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', '10.0.0.4'], ['10.0.0.4', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '10.0.0.4'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.2', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', '10.0.0.2'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', '10.0.0.3'], ['10.0.0.3', '00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', '10.0.0.3']]

        array_of_delays= [18.2, 16.4, 6.23, 8.33, 6.21, 12.2, 16.2, 4.25, 16.5, 10.3, 6.17, 13.5, 13.5, 28.4, 28.7, 34.7, 34.2, 31.6, 31.9, 39.0, 39.9, 44.8, 44.8, 46.1, 43.4, 50.7, 51.1, 62.7, 60.6, 68.1, 70.5]

        real_link_delays= {('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a'): 9.0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03'): 9.05, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05'): 8.05, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04'): 3.04, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01'): 4.06, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03'): 3.1, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b'): 9.05, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02'): 3.045, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07'): 5.0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09'): 8.05, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02'): 4.105, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04'): 6.0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b'): 9.0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09'): 9.0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06'): 9.1, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05'): 2.035, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07'): 3.085, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a'): 9.1, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06'): 2.045, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b'): 8.05, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04'): 8.1, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02'): 3.045, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05'): 8.0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01'): 6.05, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a'): 9.1, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08'): 8.0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08'): 5.0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06'): 3.055}
        
        import time
        start_time = time.time()
        measured_link_delay = link_delay_measurement_PSO(array_of_delays, node_based_path_array, debug=debug)
        end_time = time.time()
        run_duration_ms_pso = round((end_time-start_time)*1000,3)
        logger.info("PSO Algorithm (DMI Module) run duration: {}ms\n".format(run_duration_ms_pso))


        create_dir_recursively (emulation_results_dir / Path("DMI"))

        ###save all results###
        add_dic_to_file (measured_link_delay, emulation_results_dir / Path("DMI") / "measured_link_delay.txt")


        max_error_per_one_link, summation_of_all_link_delays_error,link_real_and_measured_delay= link_delay_measurement_and_comparison_PSO(array_of_delays, node_based_path_array, real_link_delays, debug=debug,save_to_file_dir= emulation_results_dir / "4.DMI_measured_link_delay.txt")

        ###writing DMI Module(PSO Algorithm) results into file
        add_dic_to_file (max_error_per_one_link, emulation_results_dir / Path("DMI") / "max_error_per_one_link.txt")
        add_dic_to_file (summation_of_all_link_delays_error, emulation_results_dir / Path("DMI") / "summation_of_all_link_delays_error.txt" )
        number_of_probes=number_of_included_links=run_duration_ms_ilp=max_len_of_probes_array=number_of_existing_links=number_of_switches=percent_of_hosts=links_monitored_percent=NUMBER_OF_HOSTS=number_of_rules=number_of_flows=0

        csv_writer_results_all.writerow([number_of_probes,number_of_included_links,run_duration_ms_ilp,max_len_of_probes_array,number_of_existing_links,number_of_switches,percent_of_hosts,links_monitored_percent,NUMBER_OF_HOSTS,number_of_rules,number_of_flows, round(max_error_per_one_link,2), round(summation_of_all_link_delays_error,2),run_duration_ms_pso])

        csv_writer_results_solved.writerow([number_of_probes,number_of_included_links,run_duration_ms_ilp,max_len_of_probes_array,number_of_existing_links,number_of_switches,percent_of_hosts,links_monitored_percent,NUMBER_OF_HOSTS,number_of_rules,number_of_flows, round(max_error_per_one_link,2), round(summation_of_all_link_delays_error,2),run_duration_ms_pso])

        if max_len_of_probes_array is min_max_length_of_routes_all_topologies_solved:
            csv_writer_barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,number_of_rules])
            csv_writer_barchart_summation_of_all_links_delay_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,summation_of_all_link_delays_error])
            csv_writer_barchart_max_link_delay_error_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,max_error_per_one_link])

            temp_sum_to_calculation_absolute_error = 0
            link_id = 1
            for item in sort_list_of_tupples_by_nth_element(link_real_and_measured_delay,0):
                link_name = item[0]
                real_delay = item[1]
                estimated_delay = item[2]
                csv_writer_barchart_real_and_measured_delay_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,real_delay,estimated_delay,link_id,'\"'+str(link_name)+'\"'])
                link_id = link_id + 1
                temp_sum_to_calculation_absolute_error = temp_sum_to_calculation_absolute_error + abs(real_delay-estimated_delay)/estimated_delay 

            absolute_percent_error = round((temp_sum_to_calculation_absolute_error/number_of_existing_links) * 100,2)
            csv_writer_absolute_error_max_len_of_route_all_solved.writerow([NUMBER_OF_HOSTS,absolute_percent_error])