from modules.path_and_flow_selector_heuristic_PSF import heuristic_for_ILP
import json
from pathlib import Path

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

import csv

###configs###
max_hop_count_path = 29
SEQUENTIAL_LEN_OF_PROBE_ARRAYS = True
#TOPOLOGY_EXCLUDE = ["Geant"]
TOPOLOGY_EXCLUDE = [" "]
DURATION_RUN_LIMIT_MS = 100000

def get_file_names_in_a_directory(dir):
    import os
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return sorted(files)

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
    # out=[]
    # for i in range(min_len,len(lst)):
    #     out.append(lst[0:i])
    # return out

def write_object_to_file(objet_to_write,dir,filename,create_parents_if_not_exists = True):
    import pathlib
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)
    f = open(Path(dir) / filename, "w+")
    f.write(str(objet_to_write))
    f.close()

def create_dir_recursively (dir):
    import pathlib
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

topology_matrix_dir =  Path(__file__).parent /  "evaluation/topologyzoo/topology_matrix"
from importlib import import_module

final_output = [] 
good_outputs = []

import progressbar as pb

"""
[
    {topo_name: "GEANT", 
     info:{
     }
    },
    {},
    {}
]
"""
for file_name in get_file_names_in_a_directory(topology_matrix_dir):
    go_out = False
    for topo_name in TOPOLOGY_EXCLUDE:
        if topo_name in file_name:
            go_out = True
            break
    if go_out:
        go_out = False
        continue

    # if not file_name.endswith(".py"):
    #     continue
    # add = str(topology_matrix_dir/file_name)
    # a = import_module  (name=file_name,package=str(topology_matrix_dir))
    # b=a.get_topology_matrix()
    final_output.append({})
    good_outputs.append({})
    final_output[-1]["topo_name"] = file_name.replace(".txt","").split("_")[0]

    topo_dir = Path("evaluation/PSF") / Path(final_output[-1]["topo_name"])
    create_dir_recursively (topo_dir)
    create_dir_recursively (topo_dir)

    with open(topology_matrix_dir/file_name) as topology_matrix_file,open(topo_dir/Path("all_"+file_name.replace(".txt",".csv")), '+w', newline='') as csv_file_all,open(topo_dir/Path("good_"+file_name.replace(".txt",".csv")), '+w', newline='') as csv_file_good:
        topology_matrix = eval(topology_matrix_file.read())
        csv_writer_all = csv.writer(csv_file_all,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)
        csv_writer_good = csv.writer(csv_file_good,delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

        csv_writer_all.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#len(length_of_probes_array)","#number_of_existing_links","#number_of_switches","#number_of_hosts","#links_monitored_percent"])
        csv_writer_good.writerow(["#number_of_probes","#number_of_included_links","#run_duration_ms","#len(length_of_probes_array)","#number_of_existing_links","#number_of_switches","#number_of_hosts","#links_monitored_percent"])

        
        
        initial_length_of_probes_array = range(2,3)
        nodeBasedPath_arrayOfList,number_of_probes,number_of_existing_links,number_of_included_links = heuristic_for_ILP(topo=topology_matrix, length_of_probes_array=initial_length_of_probes_array, debug=False)
        
        switches = set()
        for item in topology_matrix:
            if item[2]=='s':
                switches.add(item[0])
        number_of_switches = len (switches)

        number_of_hosts = int(file_name.replace(".txt","").split("_")[1])
        final_output[-1]["number_of_hosts"] = number_of_hosts
        final_output[-1]["number_of_switches"] = number_of_switches
        final_output[-1]["number_of_links"] = number_of_existing_links

        good_outputs[-1]["topo_name"] = final_output[-1]["topo_name"]
        good_outputs[-1]["number_of_hosts"] = number_of_hosts
        good_outputs[-1]["number_of_switches"] = number_of_switches
        good_outputs[-1]["number_of_links"] = number_of_existing_links

        final_output[-1]["runs_info"] = []
        good_outputs[-1]["runs_info"] = []
        
        
        all_sets = None
        path_length_array = range(2,max_hop_count_path+1)    
        if SEQUENTIAL_LEN_OF_PROBE_ARRAYS:
            all_sets = get_sequential_subsets(path_length_array)
        else:
            all_sets = get_all_subset(path_length_array)

        #initialize widgets
        widgets = ['topo: %s, hosts: %s, switches: %s, links: %s, number of probe arrays: %s --> '%(final_output[-1]["topo_name"],final_output[-1]["number_of_hosts"],good_outputs[-1]["number_of_switches"],number_of_existing_links,len(all_sets)), pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]


        #initialize timer
        timer = pb.ProgressBar(widgets=widgets, maxval=len(all_sets)).start()

        #length_of_probes_array = []
        i=0
        for length_of_probes_array in all_sets:
            import time
            start_time = time.time()
            nodeBasedPath_arrayOfList,number_of_probes,number_of_existing_links,number_of_included_links = heuristic_for_ILP(topo=topology_matrix, length_of_probes_array=length_of_probes_array, debug=False)
            end_time = time.time()
            run_duration_ms = round((end_time-start_time)*1000,3)
            links_monitored_percent = round(number_of_included_links*1.0/number_of_existing_links,2)*100
            final_output[-1]["runs_info"].append({"number_of_probes":number_of_probes,"number_of_existing_links":number_of_existing_links,"number_of_included_links":number_of_included_links,"run_duration_ms":run_duration_ms,"length_of_probes_array":length_of_probes_array,"links_monitored_percent":links_monitored_percent})
            
            csv_writer_all.writerow([number_of_probes,number_of_included_links,run_duration_ms,len(length_of_probes_array),number_of_existing_links,number_of_switches,number_of_hosts,links_monitored_percent])

            if number_of_included_links == number_of_existing_links:
                good_outputs[-1]["runs_info"].append({"number_of_probes":number_of_probes,"number_of_existing_links":number_of_existing_links,"number_of_included_links":number_of_included_links,"run_duration_ms":run_duration_ms,"length_of_probes_array":length_of_probes_array,"links_monitored_percent":links_monitored_percent})
                csv_writer_good.writerow([number_of_probes,number_of_included_links,run_duration_ms,len(length_of_probes_array),number_of_existing_links,number_of_switches,number_of_hosts,links_monitored_percent])
            i = i+1 
            timer.update(i)
            if run_duration_ms>DURATION_RUN_LIMIT_MS:
                print("duration run limit: %s"%(run_duration_ms))
                break
        write_object_to_file(final_output[-1],Path("evaluation/PSF") / Path(final_output[-1]["topo_name"]),Path("all_"+file_name))
        write_object_to_file(good_outputs[-1],Path("evaluation/PSF") / Path(final_output[-1]["topo_name"]),Path("good_"+file_name))
        # f = open(Path("evaluation/PSF") / Path(final_output[-1]["topo_name"])/ Path(file_name+".txt"), "w+")
        # f.write(str(final_output))
        # f.close()
        timer.finish()

#print (final_output)

write_object_to_file(final_output,Path("evaluation/PSF"),Path("all_"+file_name+".txt"))
write_object_to_file(good_outputs,Path("evaluation/PSF"),Path("good_"+file_name+".txt"))


# f = open(Path("evaluation/PSF") / "all_topo.txt", "w+")
# f.write(str(final_output))
# f.close()

# f = open(Path("evaluation/PSF") / "good_res.txt", "w+")
# f.write(str(good_outputs))
# f.close()


#abilene_length_of_probes_array =  range(2, 29) #[2,3,4,5,6,7]
        #abilene_topo = {('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:02', 's'): 1, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:01', 's'): 1, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:03', 's'): 1, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:01', 's'): 1, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:01', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:02', 's'): 0, ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:0b', 's'): 1, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:02', 's'): 1, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0a', 's'): 1, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:03', 's'): 1, ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:03', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05', 's'): 1, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04', 's'): 1, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:07', 's'): 1, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:04', 's'): 1, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:04', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06', 's'): 1, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05', 's'): 1, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:07', 's'): 1, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:05', 's'): 1, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:05', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:09', 's'): 1, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:06', 's'): 1, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:06', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:08', 's'): 1, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:07', 's'): 1, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:07', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09', 's'): 1, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08', 's'): 1, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:08', 's'): 0, ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:0b', 's'): 1, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:08', 's'): 1, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a', 's'): 1, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09', 's'): 1, ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:09', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0a', 's'): 0, ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:0b', 's'): 1, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0a', 's'): 1, ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:0b', 's'): 0, ('00:00:00:00:00:02', '00:00:00:00:00:00:00:02', 'h'): 1, ('00:00:00:00:00:03', '00:00:00:00:00:00:00:03', 'h'): 1}