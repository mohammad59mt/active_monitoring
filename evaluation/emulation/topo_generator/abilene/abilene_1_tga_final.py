#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call



###---Auto Generated Codes by autoTopoGenerator.py---###
import json
with open("config.json") as config_file:
    data = json.load(config_file)
###------------------------------------------------------------------###





###---Auto Generated Codes by autoTopoGenerator.py---###
def get_key_and_value_for_actual_link_delay(my_var,my_var_name):
    my_var_name_splitted=my_var_name.split("_")
    return format(int(my_var_name_splitted[1]),'00000000000016x')+"|"+format(int(my_var_name_splitted[3]),'00000000000016x'),format(int(my_var_name_splitted[3]),'00000000000016x')+"|"+format(int(my_var_name_splitted[1]),'00000000000016x'),int(my_var['delay'].replace('ms',''))
###------------------------------------------------------------------###



def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)

    info( '*** Add test hosts\n')
    th_1 = net.addHost('th_1', cls=Host, ip='10.0.0.101', defaultRoute=None)
    th_2 = net.addHost('th_2', cls=Host, ip='10.0.0.102', defaultRoute=None)
    th_3 = net.addHost('th_3', cls=Host, ip='10.0.0.103', defaultRoute=None)
    th_4 = net.addHost('th_4', cls=Host, ip='10.0.0.104', defaultRoute=None)
    th_5 = net.addHost('th_5', cls=Host, ip='10.0.0.105', defaultRoute=None)
    th_6 = net.addHost('th_6', cls=Host, ip='10.0.0.106', defaultRoute=None)
    th_7 = net.addHost('th_7', cls=Host, ip='10.0.0.107', defaultRoute=None)
    th_8 = net.addHost('th_8', cls=Host, ip='10.0.0.108', defaultRoute=None)
    th_9 = net.addHost('th_9', cls=Host, ip='10.0.0.109', defaultRoute=None)
    th_10 = net.addHost('th_10', cls=Host, ip='10.0.0.110', defaultRoute=None)
    th_11 = net.addHost('th_11', cls=Host, ip='10.0.0.111', defaultRoute=None)

    info( '*** Add test hosts and switches links\n')
    net.addLink(s1, th_1)
    net.addLink(s2, th_2)
    net.addLink(s3, th_3)
    net.addLink(s4, th_4)
    net.addLink(s5, th_5)
    net.addLink(s6, th_6)
    net.addLink(s7, th_7)
    net.addLink(s8, th_8)
    net.addLink(s9, th_9)
    net.addLink(s10, th_10)
    net.addLink(s11, th_11)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
#    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    validDelayMatrix = {}

    s_1_s_2 = {'delay':'4ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_1_s_2"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_1_s_2,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s1, s2, cls=TCLink , **s_1_s_2)


    s_2_s_4 = {'delay':'3ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_2_s_4"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_2_s_4,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s4, cls=TCLink , **s_2_s_4)


    s_4_s_1 = {'delay':'6ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_4_s_1"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_4_s_1,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s1, cls=TCLink , **s_4_s_1)


    s_2_s_3 = {'delay':'3ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_2_s_3"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_2_s_3,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s3, cls=TCLink , **s_2_s_3)


    s_3_s_11 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_3_s_11"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_3_s_11,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s11, cls=TCLink , **s_3_s_11)


    s_11_s_10 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_11_s_10"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_11_s_10,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s11, s10, cls=TCLink , **s_11_s_10)


    s_10_s_9 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_10_s_9"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_10_s_9,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s10, s9, cls=TCLink , **s_10_s_9)


    s_9_s_8 = {'delay':'8ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_9_s_8"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_9_s_8,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s9, s8, cls=TCLink , **s_9_s_8)


    s_7_s_8 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_7_s_8"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_7_s_8,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s7, s8, cls=TCLink , **s_7_s_8)


    s_7_s_6 = {'delay':'3ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_7_s_6"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_7_s_6,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s7, s6, cls=TCLink , **s_7_s_6)


    s_6_s_10 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_6_s_10"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_6_s_10,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s6, s10, cls=TCLink , **s_6_s_10)


    s_6_s_5 = {'delay':'2ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_6_s_5"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_6_s_5,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s6, s5, cls=TCLink , **s_6_s_5)


    s_5_s_11 = {'delay':'8ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_5_s_11"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_5_s_11,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s5, s11, cls=TCLink , **s_5_s_11)


    s_5_s_4 = {'delay':'8ms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == "s_5_s_4"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s_5_s_4,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s5, s4, cls=TCLink , **s_5_s_4)

    net.addLink(h1, s3)
    #net.addLink(h2, s7)



###---Auto Generated Codes by autoTopoGenerator.py---###
    import os
  
    info( '*** Add coordinator and manager hosts\n')
    coordinator_host = net.addHost(data['coordinator']['host_name'], cls=Host, ip=data['coordinator']['ip'], defaultRoute=None)
    traffic_manager_host = net.addHost(data['traffic_manager']['host_name'], cls=Host, ip=data['traffic_manager']['ip'], defaultRoute=None)

    info( '*** Add coordinator and manager switch\n')
    coordinatorandmanager_sw = net.addSwitch(data['management_switch']['name'], cls=OVSKernelSwitch,dpid=data['management_switch']['dpid']) #this switch is for connecting coordinator and controller


    info( '*** Add coordinator and manager hosts and switch links\n')
    net.addLink(coordinator_host, coordinatorandmanager_sw)
    net.addLink(traffic_manager_host, coordinatorandmanager_sw)
    net.addLink(coordinatorandmanager_sw, s1) #always connect coordinator switch to s1
###------------------------------------------------------------------###



    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s5').start([c0])
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s8').start([c0])



###---Auto Generated Codes by autoTopoGenerator.py---###

    i=0
    for host in net.hosts:
        host.setMAC(format(i+1,'00000000000012x'))
        i=i+1
        #for host in net.hosts:
        #host.popen('python3 ./packet_generator/packet_generator_agent.py')
    import time
    info( '*** Post configure coordinator and manager switch\n')#config coordinator switch, so coordinator can talk with controller
    net.get(data['management_switch']['name']).start([c0])
    os.system('ip addr flush dev %s'%(data['controller']['intf']))
    os.system('ip link set %s up'%(coordinatorandmanager_sw))
    coordinatorandmanager_sw.cmd('ovs-vsctl add-port %s %s'%(coordinatorandmanager_sw,data['controller']['intf']))
    coordinatorandmanager_sw.cmd('ifconfig %s %s'%(coordinatorandmanager_sw,data['controller']['ip']))

    info( '*** Post configure running host test agent\n')
    #for host in net.hosts:
    #   print(host.name)
#       if "ht" in host.name:
#          host.cmdPrint('python3 %s&'%(data['codeGeneration']['host_test_agent_path']))
          
          
    info( '*** Post configure coordinator and traffic manager hosts\n')#config coordinator switch, so coordinator can talk with controller
    traffic_manager_host.cmdPrint('python3 ../../modules/traffic_generator/traffic_generator_manager_TGM.py&')
    traffic_manager_host.cmdPrint('python3 ../../modules/traffic_generator/traffic_generator_manager_TGM.py --port 5050&')
    
    info( '*** Running agents on hosts\n')
    for host in net.hosts:
        if "th" in host.name:
            host.cmdPrint('python3 ../../modules/traffic_generator/traffic_generator_agent_TGA.py&')
            continue
        if "th" not in host.name and "tm_h" not in host.name and "coord_h" not in host.name:
            host.cmdPrint('python3 ../../modules/traffic_generator/traffic_generator_agent_TGA.py&')

            


    #info( '*** Enable OpenFlow13 on all switches\n')
#    for sw in net.switches:
#        sw.popen('ovs-vsctl set bridge %s protocols=OpenFlow13'%(sw))
#        time.sleep(0.1)
    

###validDelayMatrix commented###    
    switchesList = []
    for sw1 in net.switches:
        for sw2 in net.switches:
            if str(sw1.dpid)+"|"+str(sw2.dpid) not in validDelayMatrix:
                if str(sw1.dpid).strip(":")!=data['management_switch']['dpid'] and str(sw2.dpid).strip(":")!=data['management_switch']['dpid']:
                    validDelayMatrix[str(sw1.dpid)+"|"+str(sw2.dpid)]=0

    print (validDelayMatrix)
    f_actual= open("../latest/outputs/actual_link_delay_matrix.txt","w+")
    f_actual.write(str(validDelayMatrix))
    f_actual.close()
###validDelayMatrix commented###    
        
    info( '*** Adding helper arp entry to all hosts\n')
    for host in net.hosts:
        if "ht" not in host.name:
            host.popen('arp -s %s %s'%(data['helper']['ip'],data['helper']['mac']))
            time.sleep(0.2)
        
    info( '*** Waiting for 20 seconds\n')    
#    for i in range (0,20):
#        print (i)
#        time.sleep(1)
        
    info( '*** Running coordinator\n')            
#    coordinator_host.cmdPrint('python3 ../../coordinator/coordinator.py')

#    info( '*** Pinging 10.0.0.1 from all hosts\n')
    #for host in net.hosts:
#        host.cmd('ping 10.0.0.1 -c 2 -W 1')
#        time.sleep(1)
#    h1.cmd('ping 10.0.0.2 -c 2 -W1')

###------------------------------------------------------------------###



    info( '*** Post configure switches and hosts\n')



###---Auto Generated Codes by autoTopoGenerator.py---###
###------------------------------------------------------------------###


    CLI(net,script='scripts/cli.sh')
    CLI(net)


###---Auto Generated Codes by autoTopoGenerator.py---###
    #os.system('killall java &')
###------------------------------------------------------------------###



    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


