# estimated_link_delay={('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:06') : 7.82,
# ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:0b') : 7.18,
# ('00:00:00:00:00:00:00:07', '00:00:00:00:00:00:00:06') : 8.86,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:0b') : 3.94,
# ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:09') : 9.44,
# ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:08') : 9.87,
# ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:01') : 10.05,
# ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:04') : 3.74,
# ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:07') : 6.92,
# ('00:00:00:00:00:00:00:0b', '00:00:00:00:00:00:00:02') : 6.00,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:09') : 4.72,
# ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:01') : 4.61,
# ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:04') : 9.38,
# ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:0a') : 7.43,
# ('00:00:00:00:00:00:00:09', '00:00:00:00:00:00:00:04') : 4.18,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:03') : 9.97,
# ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:08') : 9.88,
# ('00:00:00:00:00:00:00:03', '00:00:00:00:00:00:00:04') : 9.78,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:05') : 9.01,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:08') : 4.93,
# ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:07') : 9.14,
# ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:06') : 10.05,
# ('00:00:00:00:00:00:00:02', '00:00:00:00:00:00:00:0b') : 5.90,
# ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:05') : 2.82,
# ('00:00:00:00:00:00:00:04', '00:00:00:00:00:00:00:0a') : 9.51,
# ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:04') : 6.15,
# ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:08') : 2.78,
# ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:06') : 2.73,
# ('00:00:00:00:00:00:00:05', '00:00:00:00:00:00:00:04') : 8.96,
# ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:06') : 2.57,
# ('00:00:00:00:00:00:00:06', '00:00:00:00:00:00:00:0a') : 8.09,
# ('00:00:00:00:00:00:00:08', '00:00:00:00:00:00:00:03') : 9.71,
# ('00:00:00:00:00:00:00:0a', '00:00:00:00:00:00:00:09') : 7.23,
# ('00:00:00:00:00:00:00:01', '00:00:00:00:00:00:00:0a') : 4.47}

import os,json
dir_path = os.path.dirname(os.path.realpath(__file__))

from pathlib import Path
base_output_path = Path(dir_path)/Path("latest")/Path("outputs")
actual_link_delay_path = base_output_path / Path("actual_link_delay_matrix.txt")

with open(actual_link_delay_path) as actual_link_delay_file:
    str_from_file = actual_link_delay_file.read().replace("\'","\"")
    actual = json.loads(str_from_file)

estimated={}
for item in estimated_link_delay:
    src=int(item[0].split(":")[-1],16)
    dst = int(item[1].split(":")[-1], 16)
    estimated[(src,dst)]=estimated_link_delay[item]
#print (estimated)

#ping_res={}
#print(type(ping_res))
#ping_res ={'10.0.0.105': [{'detailed_rtt': [11.9, 8.0, 6.8, 10.1, 8.9], 'min': 6.8, 'average': 8.45, 'match': {'dst_ip': '10.0.0.106'}, 'max': 11.9}, {'detailed_rtt': [23.3, 19.0, 18.0, 21.2, 20.0], 'min': 18.0, 'average': 19.55, 'match': {'dst_ip': '10.0.0.104'}, 'max': 23.3}], '10.0.0.106': [{'detailed_rtt': [20.8, 19.9, 19.3, 17.9, 21.3], 'min': 17.9, 'average': 20.325, 'match': {'dst_ip': '10.0.0.110'}, 'max': 21.3}, {'detailed_rtt': [31.8, 31.1, 29.9, 28.9, 27.8], 'min': 27.8, 'average': 30.425, 'match': {'dst_ip': '10.0.0.107'}, 'max': 31.8}, {'detailed_rtt': [23.2, 21.9, 22.0, 20.9, 20.6], 'min': 20.6, 'average': 21.35, 'match': {'dst_ip': '10.0.0.101'}, 'max': 23.2}, {'detailed_rtt': [23.7, 10.8, 6.6, 8.0, 7.2], 'min': 6.6, 'average': 8.15, 'match': {'dst_ip': '10.0.0.105'}, 'max': 23.7}, {'detailed_rtt': [7.9, 6.2, 10.1, 10.5, 8.0], 'min': 6.2, 'average': 9.125, 'match': {'dst_ip': '10.0.0.108'}, 'max': 10.5}], '10.0.0.102': [{'detailed_rtt': [15.8, 11.0, 11.1, 14.0, 13.2], 'min': 11.0, 'average': 12.325, 'match': {'dst_ip': '10.0.0.111'}, 'max': 15.8}], '10.0.0.101': [{'detailed_rtt': [39.8, 40.0, 38.9, 38.0, 37.2], 'min': 37.2, 'match': {'dst_ip': '10.0.0.106'}, 'average': 39.175, 'max': 40.0}, {'detailed_rtt': [19.8, 10.9, 9.9, 9.1, 9.0], 'min': 9.0, 'match': {'dst_ip': '10.0.0.110'}, 'average': 9.725, 'max': 19.8}], '10.0.0.103': [{'detailed_rtt': [35.8, 31.1, 34.6, 33.9, 32.9], 'min': 31.1, 'match': {'dst_ip': '10.0.0.108'}, 'average': 34.3, 'max': 35.8}, {'detailed_rtt': [35.8, 23.0, 22.2, 22.0, 21.4], 'min': 21.4, 'match': {'dst_ip': '10.0.0.104'}, 'average': 22.15, 'max': 35.8}], '10.0.0.110': [{'detailed_rtt': [19.9, 19.2, 18.0, 16.9, 16.6], 'min': 16.6, 'match': {'dst_ip': '10.0.0.109'}, 'average': 18.12, 'max': 19.9}, {'detailed_rtt': [23.2, 22.1, 21.2, 20.2, 19.6], 'min': 19.6, 'match': {'dst_ip': '10.0.0.106'}, 'average': 20.775, 'max': 23.2}, {'detailed_rtt': [35.8, 22.3, 23.0, 22.0, 21.0], 'min': 21.0, 'match': {'dst_ip': '10.0.0.104'}, 'average': 22.075, 'max': 35.8}, {'detailed_rtt': [18.8, 9.9, 9.2, 9.2, 8.1], 'min': 8.1, 'match': {'dst_ip': '10.0.0.101'}, 'average': 9.1, 'max': 18.8}], '10.0.0.104': [{'detailed_rtt': [15.9, 14.9, 14.1, 12.7, 16.0], 'min': 12.7, 'average': 15.225, 'match': {'dst_ip': '10.0.0.108'}, 'max': 16.0}, {'detailed_rtt': [31.7, 20.9, 24.1, 24.0, 22.8], 'min': 20.9, 'average': 22.95, 'match': {'dst_ip': '10.0.0.103'}, 'max': 31.7}, {'detailed_rtt': [19.7, 19.0, 20.5, 17.6, 21.2], 'min': 17.6, 'average': 20.1, 'match': {'dst_ip': '10.0.0.105'}, 'max': 21.2}, {'detailed_rtt': [11.1, 10.2, 9.5, 9.2, 12.1], 'min': 9.2, 'average': 10.0, 'match': {'dst_ip': '10.0.0.111'}, 'max': 12.1}, {'detailed_rtt': [31.6, 23.0, 22.0, 21.0, 23.4], 'min': 21.0, 'average': 22.35, 'match': {'dst_ip': '10.0.0.110'}, 'max': 31.6}, {'detailed_rtt': [14.4, 10.0, 9.0, 12.0, 11.0], 'min': 9.0, 'average': 10.5, 'match': {'dst_ip': '10.0.0.109'}, 'max': 14.4}], '10.0.0.107': [{'detailed_rtt': [35.9, 30.9, 31.0, 34.0, 33.0], 'min': 30.9, 'match': {'dst_ip': '10.0.0.106'}, 'average': 32.225, 'max': 35.9}, {'detailed_rtt': [39.9, 33.0, 31.8, 30.8, 33.9], 'min': 30.8, 'match': {'dst_ip': '10.0.0.111'}, 'average': 32.375, 'max': 39.9}], '10.0.0.111': [{'detailed_rtt': [7.6, 11.0, 10.0, 9.3, 11.9], 'min': 7.6, 'average': 10.55, 'match': {'dst_ip': '10.0.0.104'}, 'max': 11.9}, {'detailed_rtt': [19.8, 11.9, 13.3, 9.2, 11.7], 'min': 9.2, 'average': 11.525, 'match': {'dst_ip': '10.0.0.102'}, 'max': 19.8}, {'detailed_rtt': [23.9, 15.0, 18.0, 17.2, 16.1], 'min': 15.0, 'average': 16.575, 'match': {'dst_ip': '10.0.0.107'}, 'max': 23.9}], '10.0.0.109': [{'detailed_rtt': [27.5, 22.9, 22.0, 21.8, 21.0], 'min': 21.0, 'match': {'dst_ip': '10.0.0.108'}, 'average': 21.925, 'max': 27.5}, {'detailed_rtt': [24.0, 14.8, 14.2, 14.2, 17.2], 'min': 14.2, 'match': {'dst_ip': '10.0.0.110'}, 'average': 15.1, 'max': 24.0}, {'detailed_rtt': [15.7, 11.0, 9.9, 9.0, 8.3], 'min': 8.3, 'match': {'dst_ip': '10.0.0.104'}, 'average': 9.55, 'max': 15.7}], '10.0.0.108': [{'detailed_rtt': [16.0, 15.0, 14.1, 13.1, 15.9], 'min': 13.1, 'match': {'dst_ip': '10.0.0.104'}, 'average': 15.25, 'max': 16.0}, {'detailed_rtt': [27.6, 23.0, 22.2, 20.8, 23.9], 'min': 20.8, 'match': {'dst_ip': '10.0.0.109'}, 'average': 22.475, 'max': 27.6}, {'detailed_rtt': [24.0, 22.9, 22.1, 20.7, 24.1], 'min': 20.7, 'match': {'dst_ip': '10.0.0.103'}, 'average': 23.275, 'max': 24.1}, {'detailed_rtt': [11.7, 7.6, 6.2, 10.1, 9.1], 'min': 6.2, 'match': {'dst_ip': '10.0.0.106'}, 'average': 8.25, 'max': 11.7}]}, {'10.0.0.105': [{'dst_ip': '10.0.0.106'}, {'dst_ip': '10.0.0.104'}], '10.0.0.106': [{'dst_ip': '10.0.0.110'}, {'dst_ip': '10.0.0.107'}, {'dst_ip': '10.0.0.101'}, {'dst_ip': '10.0.0.105'}, {'dst_ip': '10.0.0.108'}], '10.0.0.102': [{'dst_ip': '10.0.0.111'}], '10.0.0.103': [{'dst_ip': '10.0.0.108'}, {'dst_ip': '10.0.0.104'}], '10.0.0.109': [{'dst_ip': '10.0.0.108'}, {'dst_ip': '10.0.0.110'}, {'dst_ip': '10.0.0.104'}], '10.0.0.110': [{'dst_ip': '10.0.0.109'}, {'dst_ip': '10.0.0.106'}, {'dst_ip': '10.0.0.104'}, {'dst_ip': '10.0.0.101'}], '10.0.0.104': [{'dst_ip': '10.0.0.108'}, {'dst_ip': '10.0.0.103'}, {'dst_ip': '10.0.0.105'}, {'dst_ip': '10.0.0.111'}, {'dst_ip': '10.0.0.110'}, {'dst_ip': '10.0.0.109'}], '10.0.0.101': [{'dst_ip': '10.0.0.106'}, {'dst_ip': '10.0.0.110'}], '10.0.0.111': [{'dst_ip': '10.0.0.104'}, {'dst_ip': '10.0.0.102'}, {'dst_ip': '10.0.0.107'}], '10.0.0.108': [{'dst_ip': '10.0.0.104'}, {'dst_ip': '10.0.0.109'}, {'dst_ip': '10.0.0.103'}, {'dst_ip': '10.0.0.106'}], '10.0.0.107': [{'dst_ip': '10.0.0.106'}, {'dst_ip': '10.0.0.111'}]}

actual_link_delay = {}
print(type(ping_res))
for src in ping_res[0]:
    for item in ping_res[0][src]:
        dst=item['match']['dst_ip']
        
        actual_link_delay = actual["|"+path[i+1].replace(":","")]
        #actual_link_delay[(int(src.split(".")[3][1:]),int(dst.split(".")[3][1:]))]=item['min']/2

#print (actual_link_delay)


compare = {}

i=0
sum=0
for item in actual_link_delay:
    err = abs(actual_link_delay[item]-estimated[item])/actual_link_delay[item]
    compare[item] = {"real":actual_link_delay[item],"estimate":estimated[item],"error":(round(err*100,3))}
    sum=sum+err
    i=i+1

avg_err = round(sum/i*100,3)

print (avg_err)
print()
print()

print (compare)