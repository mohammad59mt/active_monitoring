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

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(s1, h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    h1.cmdPrint("python -m SimpleHTTPServer 80&")

    for host in net.hosts:
       print(host.name)
       if "ht" in host.name:
          host.cmdPrint("")
          
    for sw in net.switches:
        switch_num=str(sw.name).strip("s")
        if int(switch_num)<10:
            switch_num="0"+switch_num
        temp_host_name = 'ht_'+switch_num
        temp_host_ip = '10.0.0.1'+switch_num
        temp_host=net.addHost(temp_host_name, cls=Host, ip=temp_host_ip, defaultRoute=None)
        temp_host.setIP(temp_host_ip)
        #temp_host.cmdPrint('ifconfig %s-eth0 %s/24'%(temp_host_name,temp_host_ip))
        net.addLink(temp_host,sw.name)


    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

