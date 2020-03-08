#!/usr/bin/python
import sys

from utilities import add_link_delay_modifications,add_a_host_per_switch

script_name = sys.argv[0]
mac_sort_script="""
    i=0
    for host in net.hosts:
        host.setMAC(format(i+1,'00000000000012x'))
        i=i+1
    """

def addMultiLineStringToListByIndex(multiLineStr,targetList,findLineByStr,offset=0):    
    index = [i for i in range (0,len(targetList)) if targetList[i].find(findLineByStr)>-1][0]
    multiLineStr = multiLineStr.split('\n')
    
    global script_name
    targetList[index+1+offset:index+1+offset]=["\n","###---Auto Generated Codes by %s"%(script_name)+"---###"]
    targetList[index+1+offset+2:index+1+offset+2]=multiLineStr
    targetList[index+1+offset+len(multiLineStr)+1:index+1+offset+len(multiLineStr)+1]= ["###------------------------------------------------------------------###","\n"]

    return targetList

def sortByVariableName(linesOfVariables):
   return [x[1] for x in sorted([(x.strip().split(' ')[0][1:],x) for x in linesOfVariables if x.strip()!=''],key=lambda x:int(x[0]))]

def replaceLinesOfVariablewithSorted (findStartLine,findEndLine,inputList):
   startIndex = [i for i in range (0,len(inputList)) if inputList[i].find(findStartLine)>-1][0]
   endIndex = [i for i in range (0,len(inputList)) if inputList[i].find(findEndLine)>-1][0]
   linesOfVariables = inputList[startIndex+1:endIndex-1]
   inputList[startIndex+1:endIndex-1] = sortByVariableName(linesOfVariables)
   return inputList

def main():
    import json
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='This script is for creating miniedit script in more flexible and pretty way.')
    parser.add_argument('-o', help="Path or name of ouput miniedit l2 script.",required=False)
    parser.add_argument('-i', help='Path or name of miniedit l2 script.',required=False)
    parser.add_argument('-s', dest='sort_lines_by_variable_names', action="store_true", default=True,help="Sort script lines by variable names.")
    parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
    parser.add_argument('--post-conf', dest='post_configure_script_path', help="Post configure switches and hosts script. Pass a .py file after this switch. ")
    parser.add_argument('--pre-net-start', dest='pre_network_starting_path', help="Pre-starting network script. Pass a .py file after this switch will caused to add some scripts before \"info( '*** Starting network')\" in your topology l2 script.")
    parser.add_argument('--pre-def-my-network', dest='pre_def_my_network_path',
                        help="By passing a .py file name or path after this switch, some scripts will be added before def my_network in your topology l2 script.")
    parser.add_argument('--pre-net-stop', dest='pre_network_stop_path', help="Pre-stop network script. Pass a .py file after this switch will caused to add some scripts before \"net.stop()\" in your topology l2 script.")
    parser.add_argument('--mac',help="Incremenal MAC address assignment.",dest='sort_mac_incremental', action="store_true", default=True,required=False)
    parser.add_argument('--eval', help="Insert a host per switch.", dest='insert_a_host_per_switch',
                        action="store_true", default=True, required=False)
    parser.add_argument('--delay', help="Insert a random delay per link.", dest='insert_a_random_delay_per_link',
                        action="store_true", default=False, required=False)

    args = parser.parse_args()
    input_script_path            = args.i
    sort_lines_by_variable_names = args.sort_lines_by_variable_names
    post_configure_script_path   = args.post_configure_script_path
    pre_network_starting_path    = args.pre_network_starting_path
    pre_def_my_network_path      = args.pre_def_my_network_path
    pre_network_stop_path        = args.pre_network_stop_path
    output_script_path           = args.o
    config_file_path             = args.config_file_path
    sort_mac_incremental         = args.sort_mac_incremental
    insert_a_host_per_switch     = args.insert_a_host_per_switch
    insert_a_random_delay_per_link = args.insert_a_random_delay_per_link


    if config_file_path == None:
        config_file_path             = 'config.json'
    
    configure_script="""import json
with open("%s") as config_file:
    data = json.load(config_file)
"""%(config_file_path)


    
    '''Try to load settings from the config file'''
    with open(config_file_path) as config_file:
            data = json.load(config_file)
    
    if 'codeGeneration' in data and 'base_dir' in data['codeGeneration']:
        base_dir = data['codeGeneration']['base_dir']
    else:
        import os 
        base_dir = os.path.dirname(os.path.realpath(__file__))+"/"

    if input_script_path ==None:
        if 'codeGeneration' in data and 'input_script_path' in data['codeGeneration']:    
            input_script_path      = base_dir+data['codeGeneration']['input_script_path'] 
        else:
            print ('please specify input_script_path using -i switch or set it in *.json config') 
            return
    
    if output_script_path ==None:
        if 'codeGeneration' in data and 'output_script_path' in data['codeGeneration']:
            output_script_path      = base_dir+data['codeGeneration']['output_script_path']
        else:
            print ('please specify output_script_path using -o switch or set it in *.json config') 
            return
    
    if post_configure_script_path == None and 'codeGeneration' in data and 'post_configure_script_path' in data['codeGeneration']:
        post_configure_script_path = base_dir+data['codeGeneration']['post_configure_script_path']

    if pre_def_my_network_path == None and 'codeGeneration' in data and 'pre_def_my_network_path' in data['codeGeneration']:
        pre_def_my_network_path = base_dir+data['codeGeneration']['pre_def_my_network_path']


    if pre_network_starting_path == None and 'codeGeneration' in data and 'pre_network_starting_path' in data['codeGeneration']:
        pre_network_starting_path = base_dir+data['codeGeneration']['pre_network_starting_path']

    if pre_network_stop_path == None  and 'codeGeneration' in data and 'pre_network_stop_path' in data['codeGeneration']:
        pre_network_stop_path      = base_dir+data['codeGeneration']['pre_network_stop_path']

    #script_name = sys.argv[0]
    #print (script_name)
    #if len(sys.argv)<2:
        #print("Something wents wrong, Please enter %s --h for more info."%(script_name))
        #return
    
    with open (input_script_path) as topo_file:
	    topo = topo_file.read()
    topo = topo.split('\n')


    if insert_a_random_delay_per_link:
        topo = add_link_delay_modifications(topo)
    topo = addMultiLineStringToListByIndex(configure_script,topo,"def myNetwork():",-1)

    if pre_def_my_network_path != None:
        with open(pre_def_my_network_path) as pre_def_my_network_file:
            pre_def_my_network_script = pre_def_my_network_file.read()
        topo = addMultiLineStringToListByIndex(pre_def_my_network_script, topo, "def myNetwork():", -1)


    if post_configure_script_path!=None:
        with open (post_configure_script_path) as post_configure_file:
	        post_configure_script = post_configure_file.read()
        if sort_mac_incremental:
            sort_lines_by_variable_names = True
            post_configure_script=mac_sort_script+post_configure_script
        topo = addMultiLineStringToListByIndex(post_configure_script,topo,"*** Post configure switches and hosts",-1)	




    if sort_lines_by_variable_names:
    	topo = replaceLinesOfVariablewithSorted ("*** Add switches","*** Add hosts",topo)
    	topo = replaceLinesOfVariablewithSorted ("*** Add hosts","*** Add links",topo)
        #topo = replaceLinesOfVariablewithSorted ("*** Starting switches","*** Post configure switches and hosts",topo)

    if pre_network_starting_path!=None:
        with open (pre_network_starting_path) as pre_network_file:
	        pre_network_starting = pre_network_file.read()
        topo = addMultiLineStringToListByIndex(pre_network_starting,topo,"*** Starting network",-1)	
    
    if pre_network_stop_path!=None:
        with open (pre_network_stop_path) as pre_network_stop_file:
	        pre_network_stop = pre_network_stop_file.read()
        topo = addMultiLineStringToListByIndex(pre_network_stop,topo,"net.stop",-1)	

    if  'mininet_cli_script' in data['codeGeneration']:
        mininet_cli_script = base_dir+data['codeGeneration']['mininet_cli_script']
        topo = addMultiLineStringToListByIndex("    CLI(net,script=\'%s\')"%(mininet_cli_script),topo,"CLI(net)",-1)

    if insert_a_host_per_switch:
        topo = add_a_host_per_switch(topo)

    '''write auto-generated scripts into output file'''
    with open(output_script_path, 'w') as f:
	    for item in topo:
		    f.write("%s\n" % item)

if __name__=="__main__":
    main()
