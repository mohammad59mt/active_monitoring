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
