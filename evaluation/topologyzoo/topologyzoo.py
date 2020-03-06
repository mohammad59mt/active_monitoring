import pathlib
import xml.etree.ElementTree as ET
import time

def get_file_names_in_a_directory(dir):
    import os
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files

def add_dic_to_file(dic,filepath):
    f = open(filepath, "w+")
    f.write(str(dic))
    f.close()

def __convert_to_colon_separated (a):
    #a = "0000000000000001"
    for j in range(0, int(len(a) / 2)):
        if j == 0:
            continue
        a = a[0:2 * j + j - 1] + ":" + a[2 * j + j - 1:]
    # a = "00:00:00:00:00:00:00:01"
    return a
    
def convert_id_to_dpid (id):
    """
    param id: input switch id e.g. 1

    return : output dpid e.g. 00:00:00:00:00:00:00:01
    """
    return __convert_to_colon_separated (format(id,'00000000000016x'))

def convert_id_to_mac (id):
    """
    param id: input switch id e.g. 1

    return : output dpid e.g. 00:00:00:00:00:00:00:01
    """
    return __convert_to_colon_separated (format(id,'00000000000012x'))


PERCENT_OF_HOSTS_IN_EACH_TOPO = [1,5,10,20,30]

start_time = time.time()
xml_dir =  pathlib.Path(__file__).parent /  "xml"
topolgy_matrix_dir =  pathlib.Path(__file__).parent /  "topology_matrix"

final_topo = {}
for file_name in get_file_names_in_a_directory(xml_dir):
    leaf_switches = []
    edge_counter = {}  #{00:00:00:00:00:00:00:01:2,00:00:00:00:00:00:00:02:1}
    if not file_name.endswith(".xml"):
        continue
    root = ET.parse(xml_dir/file_name).getroot()
    switches = []
    for item in root.getchildren():
        for i in item.getchildren():
            # print (i.attrib)

            if 'id' in i.keys():
                switches.append(convert_id_to_dpid(int(i.attrib['id'])+1))
    
    for sw1 in switches:
        for sw2 in switches:
            edge_counter[sw1] = 0
            # final_topo[(sw1,sw2,'s')] = 0
            # final_topo[(sw2,sw1,'s')] = 0

    for item in root.getchildren():
        for i in item.getchildren():
            if 'source' in i.keys() and 'target' in  i.keys():
                src_sw_dpid = convert_id_to_dpid(int(i.attrib['source'])+1)
                dst_sw_dpid = convert_id_to_dpid(int(i.attrib['target'])+1)
                edge_counter[src_sw_dpid]=edge_counter[src_sw_dpid]+1
                final_topo[(src_sw_dpid,dst_sw_dpid,'s')] = 1
                final_topo[(dst_sw_dpid,src_sw_dpid,'s')] = 1

    for sw,edge_count in edge_counter.items():
        if edge_count == 1:
            leaf_switches.append(sw)
            
    min_percent_avaiable  = int(1*100/len(switches))
    max_percent_available = int(len(leaf_switches)*100/len(switches)) 
    #print (len(leaf_switches)*100/len(switches))

    ##connect hosts to the topo##
    for percent_of_host in PERCENT_OF_HOSTS_IN_EACH_TOPO:
        if percent_of_host < min_percent_avaiable:
            continue

        #import ipaddress
        #ip_address_int = int(ipaddress.ip_address('10.0.0.1')) #167772161
        #host_mac_int = 1
        # add a host to every switches
        added_host_counter = 0
        for sw in leaf_switches:
            #host_ip =  ipaddress.ip_address(ip_address_int).__str__()
            host_mac = sw[6:]
            final_topo[(host_mac,sw,'h')] = 1
            added_host_counter = added_host_counter+1
            host_percent = added_host_counter*100/len(switches)
            if host_percent>=percent_of_host:
                break
            #ip_address_int = ip_address_int + 1
        out_file_name = file_name.replace('.graphml.xml','')+"_"+str(percent_of_host)+".txt"
        add_dic_to_file(final_topo,topolgy_matrix_dir/out_file_name)
        print ("%s converted to topology_matrix --> %s"%(file_name,out_file_name))

print ("\nDone! It only took %s ms"%(round((time.time()-start_time)*1000)))

    # print (root)
    # file_to_whois_dir = todo_list_dir+"/"+file_name
    # os.system("%s -i %s -o %s --allorgs --append"%(WHOIS_COMMAND,file_to_whois_dir,final_output_path))
    # os.system("cp %s %s"%(file_to_whois_dir,final_output_dir))