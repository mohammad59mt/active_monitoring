import pathlib
import xml.etree.ElementTree as ET
import time


NUMBER_OF_HOSTS_IN_EACH_TOPO = range(1,6)
MAX_PERCENT_OF_HOST = 100


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


def convert_topologyzoo_xml_to_topology_matrix(topology_zoo_xml_dir,topology_matrix_dir):
    for file_name in get_file_names_in_a_directory(topology_zoo_xml_dir):      
        if not file_name.endswith(".xml"):
            continue

        topology_matrix_object = TopologyZooXML(topology_zoo_xml_dir/file_name)
        
        ##connect hosts to the topo##
        for number_of_hosts in NUMBER_OF_HOSTS_IN_EACH_TOPO:
            final_topo=topology_matrix_object.get_topology_matrix(number_of_hosts)
            host_percent = number_of_hosts*100/len(topology_matrix_object.switches)

            out_file_name = ""
            if MAX_PERCENT_OF_HOST <100 :
                out_file_name = file_name.replace('.graphml.xml','')+"_"+str(number_of_hosts)+"_host_"+str(round(host_percent))+"_percent.txt"
            else:
                out_file_name = file_name.replace('.graphml.xml','')+"_"+str(number_of_hosts)+"_hosts"+".txt"

            add_dic_to_file(final_topo,topology_matrix_dir/out_file_name)
            print ("%s converted to topology_matrix --> %s"%(file_name,out_file_name))

            if host_percent > MAX_PERCENT_OF_HOST:
                break
                

class TopologyZooXML:
    def __init__(self,path):
        self.topology_zoo_xml_path = path
        self.root = ET.parse(path).getroot()
        self.switches = self.get_switches()
        self.edge_counter,self.final_topo = self.get_edge_counter()
        self.edge_switches = self.get_edge_swithes()

    def get_switches (self):
        switches = []
        for item in self.root.getchildren():
            for i in item.getchildren():
                if 'id' in i.keys():
                    switches.append(convert_id_to_dpid(int(i.attrib['id'])+1))
        return switches
    
   
    def get_edge_counter(self):
        edge_counter = {}  #{00:00:00:00:00:00:00:01:2,00:00:00:00:00:00:00:02:1}
        final_topo = {}
        for sw1 in self.switches:
        #   for sw2 in switches:
            edge_counter[sw1] = 0
        
        for item in self.root.getchildren():
            for i in item.getchildren():
                if 'source' in i.keys() and 'target' in  i.keys():
                    src_sw_dpid = convert_id_to_dpid(int(i.attrib['source'])+1)
                    dst_sw_dpid = convert_id_to_dpid(int(i.attrib['target'])+1)
                    edge_counter[src_sw_dpid]=edge_counter[src_sw_dpid]+1
                    edge_counter[dst_sw_dpid]=edge_counter[dst_sw_dpid]+1
                    final_topo[(src_sw_dpid,dst_sw_dpid,'s')] = 1
                    final_topo[(dst_sw_dpid,src_sw_dpid,'s')] = 1
        return edge_counter,final_topo


    def get_edge_swithes(self):
        edge_switches = []
        for sw,edge_count in self.edge_counter.items():
            if edge_count is  1 or 2:
                edge_switches.append(sw)
        return edge_switches

    def get_topology_matrix (self,number_of_hosts):
        ##connect hosts to the topo##
        added_host_counter = 0
        for sw in self.edge_switches:
            host_mac = sw[6:]
            self.final_topo[(host_mac,sw,'h')] = 1
            added_host_counter = added_host_counter+1
           # host_percent = added_host_counter*100/len(self.switches)
        
            if added_host_counter == number_of_hosts:
                break
        return self.final_topo


if __name__=="__main__":
    start_time = time.time()
    xml_dir =  pathlib.Path(__file__).parent /  "xml"
    topolgy_matrix_dir =  pathlib.Path(__file__).parent /  "topology_matrix"

    convert_topologyzoo_xml_to_topology_matrix (xml_dir,topolgy_matrix_dir)
    print ("\nDone! It only took %s ms"%(round((time.time()-start_time)*1000)))    