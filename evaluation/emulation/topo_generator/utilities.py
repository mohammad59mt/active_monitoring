def conv_number_to_mac(number):
    return format(number,'00000000000012x')


def add_mac_info_to_host_definition(inputList):
    host_definition_lines = get_lines_between_two_line("*** Add hosts","*** Add links",inputList)
    # i=0
    # for item in host_definition_lines:
    #     if item is "\n" or item is " ":
    #         del host_definition_lines[i]
    #     i=i+1

    i = 0
    print (host_definition_lines)
    for l in host_definition_lines:
        temp = l.split('\'')
        print (temp)
        host_index = temp[1][1:]
        print(host_index)
        mac = format(int(host_index), '00000000000012x')
        temp.insert(4,  mac)
        temp.insert(4, ", mac=")
        host_definition_lines[i]="\'".join(temp)
        #return "".join(temp)
        i=i+1
    return replace_lines_between_two_lines("*** Add hosts","*** Add links",inputList,host_definition_lines)

def replace_lines_between_two_lines (findStartLine,findEndLine,inputList, str_to_replace):
   startIndex = [i for i in range (0,len(inputList)) if inputList[i].find(findStartLine)>-1][0]
   endIndex = [i for i in range (0,len(inputList)) if inputList[i].find(findEndLine)>-1][0]
   inputList[startIndex+1:endIndex-1] = str_to_replace
   return inputList

def get_lines_between_two_line(start_line_str,end_line_str,inputList):
    startIndex = [i for i in range(0, len(inputList)) if inputList[i].find(start_line_str) > -1][0]
    endIndex = [i for i in range(0, len(inputList)) if inputList[i].find(end_line_str) > -1][0]
    linesOfVariables = inputList[startIndex + 1:endIndex - 1]
    return linesOfVariables

def add_link_delay_modifications(inputList):
    link_delay_lines = get_lines_between_two_line("*** Add links","*** Starting network",inputList)


    from random import seed
    from random import randint
    seed(1)

#    evaluation_host_counter = 1
    i = 0
    for item in link_delay_lines:
        if "net.addLink(h" in item:
            continue
        if item.strip() == "":
            pass

        first_sw_name=item.split("(")[1].split(",")[0].strip()
        second_sw_name=item.split("(")[1].split(",")[1].strip()[:-1]
        old_var_name = first_sw_name+ second_sw_name

        item = item + ")"

        new_var_name = old_var_name.strip().replace("s", "_s_")[1:]

        item = item.replace(old_var_name, new_var_name)

        link_delay=randint(2, 10)
#        link_delay=1

        script_to_insert = """
    %s = {'delay':'%sms'}
    my_var_name = [ k for k,v in locals().iteritems() if k == \"%s\"][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(%s,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
%s, cls=TCLink , **%s)
""" % (new_var_name, link_delay, new_var_name, new_var_name, item.strip(")"),new_var_name)

       

#         script_to_insert = """
#     %s = {'delay':'%sms'}
#     my_var_name = [ k for k,v in locals().iteritems() if k == \"%s\"][0]
#     k1,k2,v = get_key_and_value_for_actual_link_delay(%s,my_var_name)
#     validDelayMatrix [k1] =v
#     validDelayMatrix [k2] =v
# %s, cls=TCLink , **%s)
#     %s = net.addHost('%s', cls=Host, ip='%s', defaultRoute=None)
#     net.addLink(%s,%s)
#     %s = net.addHost('%s', cls=Host, ip='%s', defaultRoute=None)
#     net.addLink(%s,%s)
# """ % (new_var_name, randint(2, 10), new_var_name, new_var_name, item.strip(")"),new_var_name,first_sw_host_name,first_sw_host_name,first_host_ip,first_sw_name,first_sw_host_name,second_sw_host_name,second_sw_host_name,second_host_ip,second_sw_name,second_sw_host_name)

        link_delay_lines[i] = script_to_insert
        i = i + 1


    link_delay_lines.insert(0, "    validDelayMatrix = {}")

    return replace_lines_between_two_lines("*** Add links", "*** Starting network", inputList,
                                           link_delay_lines)


def add_a_host_per_switch (inputList):
    sw_definition_lines = get_lines_between_two_line("*** Add switches", "*** Add hosts", inputList)


    test_host_definition_lines_str = """
    info( '*** Add test hosts\\n')"""
    test_host_add_link_lines_str = """
    info( '*** Add test hosts and switches links\\n')"""
    i = 0
    for item in sw_definition_lines:
        # if "net.addLink(h" in item:
        #     continue
        if item.strip() == "":
            pass

        sw_name=item.split("=")[0].strip()
        sw_number = sw_name.strip("s")
        test_host_name = "th_"+sw_number
        if int(sw_number)<10:
            sw_number = "0"+sw_number
        test_host_ip = "10.0.0.1"+sw_number

        test_host_definition_lines_str = test_host_definition_lines_str+"""
    %s = net.addHost('%s', cls=Host, ip='%s', defaultRoute=None)"""%(test_host_name,test_host_name,test_host_ip)
        test_host_add_link_lines_str = test_host_add_link_lines_str + """
    net.addLink(%s, %s)"""%(sw_name,test_host_name)

        final_list = sw_definition_lines+ test_host_definition_lines_str.split("\n")+test_host_add_link_lines_str.split("\n")

    return replace_lines_between_two_lines("*** Add switches", "*** Add hosts", inputList,
                                               final_list)


topo = """
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
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s39 = net.addSwitch('s39', cls=OVSKernelSwitch)
    s20 = net.addSwitch('s20', cls=OVSKernelSwitch)
    s27 = net.addSwitch('s27', cls=OVSKernelSwitch)
    s35 = net.addSwitch('s35', cls=OVSKernelSwitch)
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s22 = net.addSwitch('s22', cls=OVSKernelSwitch)
    s26 = net.addSwitch('s26', cls=OVSKernelSwitch)
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s36 = net.addSwitch('s36', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s18 = net.addSwitch('s18', cls=OVSKernelSwitch)
    s19 = net.addSwitch('s19', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s37 = net.addSwitch('s37', cls=OVSKernelSwitch)
    s40 = net.addSwitch('s40', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s32 = net.addSwitch('s32', cls=OVSKernelSwitch)
    s33 = net.addSwitch('s33', cls=OVSKernelSwitch)
    s28 = net.addSwitch('s28', cls=OVSKernelSwitch)
    s23 = net.addSwitch('s23', cls=OVSKernelSwitch)
    s38 = net.addSwitch('s38', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s24 = net.addSwitch('s24', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s30 = net.addSwitch('s30', cls=OVSKernelSwitch)
    s34 = net.addSwitch('s34', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch)
    s21 = net.addSwitch('s21', cls=OVSKernelSwitch)
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch)
    s31 = net.addSwitch('s31', cls=OVSKernelSwitch)
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch)
    s25 = net.addSwitch('s25', cls=OVSKernelSwitch)
    s29 = net.addSwitch('s29', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h28 = net.addHost('h28', cls=Host, ip='10.0.0.28', defaultRoute=None)
    h24 = net.addHost('h24', cls=Host, ip='10.0.0.24', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h33 = net.addHost('h33', cls=Host, ip='10.0.0.33', defaultRoute=None)
    h19 = net.addHost('h19', cls=Host, ip='10.0.0.19', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h25 = net.addHost('h25', cls=Host, ip='10.0.0.25', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
    h35 = net.addHost('h35', cls=Host, ip='10.0.0.35', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h17 = net.addHost('h17', cls=Host, ip='10.0.0.17', defaultRoute=None)
    h21 = net.addHost('h21', cls=Host, ip='10.0.0.21', defaultRoute=None)
    h36 = net.addHost('h36', cls=Host, ip='10.0.0.36', defaultRoute=None)
    h27 = net.addHost('h27', cls=Host, ip='10.0.0.27', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h34 = net.addHost('h34', cls=Host, ip='10.0.0.34', defaultRoute=None)
    h29 = net.addHost('h29', cls=Host, ip='10.0.0.29', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h37 = net.addHost('h37', cls=Host, ip='10.0.0.37', defaultRoute=None)
    h30 = net.addHost('h30', cls=Host, ip='10.0.0.30', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    h22 = net.addHost('h22', cls=Host, ip='10.0.0.22', defaultRoute=None)
    h40 = net.addHost('h40', cls=Host, ip='10.0.0.40', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
    h26 = net.addHost('h26', cls=Host, ip='10.0.0.26', defaultRoute=None)
    h23 = net.addHost('h23', cls=Host, ip='10.0.0.23', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)
    h31 = net.addHost('h31', cls=Host, ip='10.0.0.31', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
    h20 = net.addHost('h20', cls=Host, ip='10.0.0.20', defaultRoute=None)
    h32 = net.addHost('h32', cls=Host, ip='10.0.0.32', defaultRoute=None)
    h38 = net.addHost('h38', cls=Host, ip='10.0.0.38', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h18 = net.addHost('h18', cls=Host, ip='10.0.0.18', defaultRoute=None)
    h39 = net.addHost('h39', cls=Host, ip='10.0.0.39', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s40, s1)
    net.addLink(s40, s2)
    net.addLink(s40, s4)
    net.addLink(s40, s34)
    net.addLink(s40, s30)
    net.addLink(s1, s33)
    net.addLink(s2, s32)
    net.addLink(s2, s35)
    net.addLink(s2, s4)
    net.addLink(s2, s38)
    net.addLink(s2, s36)
    net.addLink(s2, s31)
    net.addLink(s3, s10)
    net.addLink(s3, s19)
    net.addLink(s3, s4)
    net.addLink(s3, s5)
    net.addLink(s3, s30)
    net.addLink(s4, s5)
    net.addLink(s4, s6)
    net.addLink(s4, s8)
    net.addLink(s4, s16)
    net.addLink(s4, s17)
    net.addLink(s4, s29)
    net.addLink(s4, s31)
    net.addLink(s5, s23)
    net.addLink(s6, s7)
    net.addLink(s7, s8)
    net.addLink(s7, s25)
    net.addLink(s7, s34)
    net.addLink(s8, s9)
    net.addLink(s8, s25)
    net.addLink(s9, s25)
    net.addLink(s9, s18)
    net.addLink(s9, s29)
    net.addLink(s9, s15)
    net.addLink(s11, s13)
    net.addLink(s12, s14)
    net.addLink(s12, s20)
    net.addLink(s12, s13)
    net.addLink(s12, s22)
    net.addLink(s12, s15)
    net.addLink(s13, s22)
    net.addLink(s13, s14)
    net.addLink(s15, s29)
    net.addLink(s16, s34)
    net.addLink(s17, s30)
    net.addLink(s21, s27)
    net.addLink(s22, s26)
    net.addLink(s22, s27)
    net.addLink(s22, s23)
    net.addLink(s23, s29)
    net.addLink(s24, s25)
    net.addLink(s24, s34)
    net.addLink(s27, s28)
    net.addLink(s28, s29)
    net.addLink(s30, s39)
    net.addLink(s32, s34)
    net.addLink(s33, s34)
    net.addLink(s35, s36)
    net.addLink(s36, s37)
    net.addLink(s38, s39)
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(h5, s5)
    net.addLink(h6, s6)
    net.addLink(h7, s7)
    net.addLink(h8, s8)
    net.addLink(h9, s9)
    net.addLink(h10, s10)
    net.addLink(h11, s11)
    net.addLink(h12, s12)
    net.addLink(h13, s13)
    net.addLink(h14, s14)
    net.addLink(h15, s15)
    net.addLink(h16, s16)
    net.addLink(h17, s17)
    net.addLink(h18, s18)
    net.addLink(h19, s19)
    net.addLink(h20, s20)
    net.addLink(h21, s21)
    net.addLink(h22, s22)
    net.addLink(h23, s23)
    net.addLink(h24, s24)
    net.addLink(h25, s25)
    net.addLink(h26, s26)
    net.addLink(h27, s27)
    net.addLink(h28, s28)
    net.addLink(h29, s29)
    net.addLink(h30, s30)
    net.addLink(h31, s31)
    net.addLink(h32, s32)
    net.addLink(h33, s33)
    net.addLink(h34, s34)
    net.addLink(h35, s35)
    net.addLink(h36, s36)
    net.addLink(h37, s37)
    net.addLink(h38, s38)
    net.addLink(h39, s39)
    net.addLink(h40, s40)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s39').start([c0])
    net.get('s20').start([c0])
    net.get('s27').start([c0])
    net.get('s35').start([c0])
    net.get('s12').start([c0])
    net.get('s7').start([c0])
    net.get('s22').start([c0])
    net.get('s26').start([c0])
    net.get('s13').start([c0])
    net.get('s2').start([c0])
    net.get('s36').start([c0])
    net.get('s1').start([c0])
    net.get('s18').start([c0])
    net.get('s19').start([c0])
    net.get('s4').start([c0])
    net.get('s11').start([c0])
    net.get('s5').start([c0])
    net.get('s37').start([c0])
    net.get('s40').start([c0])
    net.get('s10').start([c0])
    net.get('s15').start([c0])
    net.get('s3').start([c0])
    net.get('s32').start([c0])
    net.get('s33').start([c0])
    net.get('s28').start([c0])
    net.get('s23').start([c0])
    net.get('s38').start([c0])
    net.get('s9').start([c0])
    net.get('s24').start([c0])
    net.get('s8').start([c0])
    net.get('s30').start([c0])
    net.get('s34').start([c0])
    net.get('s6').start([c0])
    net.get('s14').start([c0])
    net.get('s21').start([c0])
    net.get('s16').start([c0])
    net.get('s31').start([c0])
    net.get('s17').start([c0])
    net.get('s25').start([c0])
    net.get('s29').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
"""

if __name__ == '__main__':
    topo = topo.split('\n')
    add_link_delay_modifications(topo)
