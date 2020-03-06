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

