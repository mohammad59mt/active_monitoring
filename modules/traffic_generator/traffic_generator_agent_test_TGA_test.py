from flask import Flask, json,request
import os, subprocess
import re
import statistics
import math
from scipy.stats import norm

# companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)
#interval='u1000000'
interval='0.2' #min 200ms
count ='20'
# @api.route('/traffic/start', methods=['GET'])
# def get_companies():
#   return json.dumps(companies)

@api.route('/traffic/agent/start', methods=['POST'])
def post_companies():
    traffic_matrix = request.get_json()

    """traffic_matrix sample = {"dst_ip":"10.0.0.101"}"""
#    print ("traffic_matrix: ",traffic_matrix)
    hping_result = []
    final_output = []
    dst_ip = ""
    #ip_tos = ""
    #ip_protocol = ""
    #flow_label=0
    for traffic in traffic_matrix:
#      print ("traffic: ", traffic)
      
      dst_ip = traffic['dst_ip']
     # ip_tos = traffic['ip_tos']
#      ip_protocol = traffic['ip_protocol']
#      flow_label = traffic['flow_label']
      
      #res = _run_hping3 (str(ip_tos),'50','u100',dst_ip)
      global interval,count
      res = _run_simple_ping (count,interval,dst_ip)
#      print ("res: ",res)
      #hping_result.append(res)
      rtt_matrix = _calc_rtt (res)
#      print ("rtt_matrix: ",rtt_matrix)
      min_rtt ,average_rtt, max_rtt = _calc_rtt_stats(rtt_matrix)
      rtt_stats = {"match":{"dst_ip":dst_ip},"min":min_rtt,"average":average_rtt,"max":max_rtt,"detailed_rtt":rtt_matrix}
#      print ("rtt_stats: ",rtt_stats)
      final_output.append(rtt_stats)
#      print ("rtt_stats: ",rtt_stats)
    
    return json.dumps(final_output), 201

def _run_hping3 (tos,count_of_each_probe,delay_ms_between_each_probe,destination_ip):
  #return _run_command(['ls', '-l'])
  #return _run_command(['hping3','--icmp','--tos',tos,'-c',str(count_of_each_probe),'-i',str(delay_ms_between_each_probe),destination_ip])
#  command ='hping3 --icmp --tos %s -c %s -i %s %s'%(format(int(tos),'02x'),str(count_of_each_probe),str(delay_ms_between_each_probe),destination_ip)
  command ='ping -Q %s -c %s -i %s %s'%(format(int(tos),'02x'),str(count_of_each_probe),str(delay_ms_between_each_probe),destination_ip)

#  print (command)
  return _run_command(command)

def _run_simple_ping (count_of_each_probe,delay_ms_between_each_probe,destination_ip):
  #return _run_command(['ls', '-l'])
  #return _run_command(['hping3','--icmp','--tos',tos,'-c',str(count_of_each_probe),'-i',str(delay_ms_between_each_probe),destination_ip])
  command ='ping -c %s -i %s %s'%(str(count_of_each_probe),str(delay_ms_between_each_probe),destination_ip)
  print (command)
  return _run_command(command)

def _run_command (command_list):
  #subprocess.check_output(['ls', '-l'])    
  process = subprocess.Popen(command_list,#"hping3 --icmp --tos ff -c 1 -i u100 localhost", 
          stdout=subprocess.PIPE, 
          shell=True
          )

  stdout,stderr = process.communicate()
  process.wait()
  
  return stdout

def _calc_rtt(hping_result):
#  print ("_calc_rtt(hping_result)")
  #print ("hping_result: ",hping_result)
  hping_result = hping_result.decode('utf8')
  #print ("hping_result: ",hping_result)
  arrayofrtt = hping_result.split("\n")
  #print ("arrayofrtt: ",arrayofrtt)
  rtt_matrix = []
  for i in range(1,len(arrayofrtt)-1):
    if "time=" in arrayofrtt[i] :
      rtt_matrix.append(float(re.search(r"time=(\d+\.*\d+)", arrayofrtt[i]).group(1)))
  #print ("rtt_matrix: ",rtt_matrix)
  return rtt_matrix


def _calc_rtt_stats(rtt_matrix):
  valid_rtt_matrix = GetXPercentMedianInNormalDistribution(rtt_matrix,0.8) #remove 10 percent up and down in norml distribution
  average_rtt = statistics.mean(valid_rtt_matrix)
  min_rtt = sorted(rtt_matrix,key=float)[0]
  max_rtt = sorted(rtt_matrix,key=float)[-1]
  return min_rtt ,average_rtt, max_rtt

def __findRange(mean,variance,percent):
    return (__findXforCdf(mean,variance,(1-percent)/2),__findXforCdf(mean,variance,1-((1-percent)/2)))

def __findXforCdf(mean,variance,cdf):
    return norm.ppf(cdf, loc=mean, scale=math.sqrt(variance))

def GetXPercentMedianInNormalDistribution (input,percentOfWantedData):
    mean = statistics.mean(input)
    variance = statistics.variance(input)
    #print(mean)
    #print(variance)
    #print(math.sqrt(variance))
    validRange = __findRange(mean,variance,percentOfWantedData)
    newdata = [x for x in input if x>validRange[0] and x<validRange[1]]
    #print(validRange)
    #print(newdata)
    mean2 = statistics.mean(newdata)
    variance2 = statistics.variance(newdata)
    #print(mean2)
    #print(variance2)
    #print(math.sqrt(variance2))
    return newdata

if __name__ == '__main__':
  import json
  import sys
  import argparse
  parser = argparse.ArgumentParser(description='This script is for running packet generator agent on desired hosts. This agent recieves command via rest api from packet generator manager.')
  parser.add_argument('--config', dest='config_file_path', help="*.json config file path.")
  parser.add_argument('--port', dest='port', help="Listen port.")

  args = parser.parse_args()
  config_file_path             = args.config_file_path
  listen_port                  = args.port  
  
  
  if config_file_path != None:
    with open(config_file_path) as config_file:
      data = json.load(config_file)
  
    if listen_port == None:
      if 'agents' in data and 'port' in data['agents']:
        listen_port=data['agents']['port']
      else:
        listen_port=5000
  
  api.run(host="0.0.0.0",port=listen_port)