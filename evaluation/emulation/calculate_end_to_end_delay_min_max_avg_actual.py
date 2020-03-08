import json
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

from pathlib import Path

def calc_results():
    base_output_path = Path(dir_path)/Path("latest")/Path("outputs")
    end_to_end_delay_file_path = base_output_path/Path("3.end_to_end_delay_matrix.txt")
    actual_link_delay_path = base_output_path / Path("actual_link_delay_matrix.txt")
    pathes_path = base_output_path/ Path("2.Pathes.txt")
    end_to_end_delays = base_output_path / Path("end_to_end_delay_min_max_avg_actual.txt")
    '''Try to load settings from the config file'''
    with open(end_to_end_delay_file_path) as end_to_end_delay_file:
        str_from_file = end_to_end_delay_file.read().replace("\'","\"")
        l = json.loads(str_from_file)

    with open(actual_link_delay_path) as actual_link_delay_file:
        str_from_file = actual_link_delay_file.read().replace("\'","\"")
        actual = json.loads(str_from_file)

    with open(pathes_path) as pathes_file:
        str_from_file = pathes_file.read().replace("\'","\"")
        pathes = json.loads(str_from_file)

    print ("len(l): ",len(l))
    average=[]
    for item in l:
        for i in item.values():
            average.append(int(i["average"]))

    min=[]
    for item in l:
        for i in item.values():
            min.append(int(i["min"]))

    max=[]
    for item in l:
        for i in item.values():
            max.append(int(i["max"]))

    actual_res = []


    j=0
    print (len(pathes))
    for path in pathes:
        j=j+1
        if j == 4:
            print("here")
        delay=0
        for i in range(1,len(path)-2):
            #print (path[i].replace(":","")+"|"+path[i+1].replace(":",""))
            #print (actual[path[i].replace(":","")+"|"+path[i+1].replace(":","")])
            delay = delay+actual[path[i].replace(":","")+"|"+path[i+1].replace(":","")]
        actual_res.append (delay)

    delays = """actual: %s\nmin: %s\nmax: %s\naverage: %s\n
    """%(actual_res,min,max,average)
    print ("actual: " ,actual_res)
    print ("min: ",min)
    print ("max: ",max)
    print ("average: ",average)


    f = open(end_to_end_delays, "w+")
    f.write(str(delays))
    f.close()

calc_results()
