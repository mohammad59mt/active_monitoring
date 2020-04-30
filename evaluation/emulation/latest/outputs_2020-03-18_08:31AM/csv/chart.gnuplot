set term png
set terminal png linewidth 2
set grid
set ytics nomirror


set key left top
set output 'eval_Abilene_Max_Length_of_Routes_Number_of_Required_Flows.png'
set yrange [0:40]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Monitoring Overhead (Number of Flows)'
plot 'solved_abilene_1.csv' u 4:11 w lp t '1 Monitoring node', 'solved_abilene_2.csv' u 4:11 w lp t '2 Monitoring node','solved_abilene_3.csv' u 4:11 w lp t '3 Monitoring node','solved_abilene_4.csv' u 4:11 w lp t '4 Monitoring node','solved_abilene_5.csv' u 4:11 w lp t '5 Monitoring node'


set key right bottom
set output 'eval_Abilene_Max_Length_of_Routes_Links_Monitored.png'
set yrange [0:100]
set xrange [2:15]
set xlabel 'Max Length of Routes'
set ylabel 'Links Monitored (%)'
plot 'all_abilene_1.csv' u 4:8 w lp t '1 Monitoring node', 'all_abilene_2.csv' u 4:8 w lp t '2 Monitoring node','all_abilene_3.csv' u 4:8 w lp t '3 Monitoring node','all_abilene_4.csv' u 4:8 w lp t '4 Monitoring node','all_abilene_5.csv' u 4:8 w lp t '5 Monitoring node'



set key top left
set output 'eval_Abilene_Max_Length_of_Routes_Execution_time_ILP.png'
set yrange [0:*]
set xrange [2:15]
set xlabel 'Max Length of Routes'
set ylabel 'Execution Time of ILP (ms)'
plot 'all_abilene_1.csv' u 4:3 w lp t '1 Monitoring node', 'all_abilene_2.csv' u 4:3 w lp t '2 Monitoring node','all_abilene_3.csv' u 4:3 w lp t '3 Monitoring node','all_abilene_4.csv' u 4:3 w lp t '4 Monitoring node','all_abilene_5.csv' u 4:3 w lp t '5 Monitoring node'



set key top left
set output 'eval_Abilene_Max_Length_of_Routes_Number_of_Required_Rules.png'
set title 'Abilene'
set yrange [0:170]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Monitoring Overhead (Number of Rules)'
plot 'solved_abilene_1.csv' u 4:10 w lp t '1 Monitoring node', 'solved_abilene_2.csv' u 4:10 w lp t '2 Monitoring node','solved_abilene_3.csv' u 4:10 w lp t '3 Monitoring node','solved_abilene_4.csv' u 4:10 w lp t '4 Monitoring node','solved_abilene_5.csv' u 4:10 w lp t '5 Monitoring node'


set key left top
set output 'eval_Abilene_Max_Length_of_Max_error_per_one_link.png'
set title 'Abilene'
set yrange [0:15]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Max Error Per One Link (ms)'
plot 'solved_abilene_1.csv' u 4:12 w lp t '1 Monitoring node', 'solved_abilene_2.csv' u 4:12 w lp t '2 Monitoring node','solved_abilene_3.csv' u 4:12 w lp t '3 Monitoring node','solved_abilene_4.csv' u 4:12 w lp t '4 Monitoring node','solved_abilene_5.csv' u 4:12 w lp t '5 Monitoring node'


set key left bottom
set output 'eval_Abilene_Max_Length_of_Routes_Execution_time_PSO.png'
set yrange [0:10]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Execution time of PSO (s)'
plot 'solved_abilene_1.csv' u 4:($14/1000) w lp t '1 Monitoring node', 'solved_abilene_2.csv' u 4:($14/1000) w lp t '2 Monitoring node','solved_abilene_3.csv' u 4:($14/1000) w lp t '3 Monitoring node','solved_abilene_4.csv' u 4:($14/1000) w lp t '4 Monitoring node','solved_abilene_5.csv' u 4:($14/1000) w lp t '5 Monitoring node'






set key left top
set output 'eval_Abilene_Max_Length_of_Summation_of_All_Links_Error.png'
set yrange [0:130]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Summation of All Link Delays Error (ms)'
plot 'solved_abilene_1.csv' u 4:13 w lp t '1 Monitoring node', 'solved_abilene_2.csv' u 4:13 w lp t '2 Monitoring node','solved_abilene_3.csv' u 4:13 w lp t '3 Monitoring node','solved_abilene_4.csv' u 4:13 w lp t '4 Monitoring node','solved_abilene_5.csv' u 4:13 w lp t '5 Monitoring node'


set key left top
set output 'eval_barchart_Average_Percent_of_Rules_to_Switch_Rule_Capacity_Ratio_max_len_of_route_11.png'

set yrange [0:20]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Hosts'
set boxwidth 0.5
set style fill solid
#set linetype 1 lc rgb "green"
set y2range [0:0.335]
set y2tics 0.05
set y2label 'Average Percent of Rules to Switch Rule Capacity Ratio'
#set linetype 2 lc rgb "blue"
plot "barchart_bar_average_number_of_rules_per_switch_max_len_of_route_all_solved.csv" using 1:($2/11) with boxes title "Number of Rules per Switch",\
"" using 1:(($2/65280)*100) axes x1y2  w lp title "Percent of Rules per Switch"
unset y2label
unset y2tics

#set y2tics         # make the right y-axis 'visible'
#unset multiplot
set key left top
set output 'eval_bar_min_length_of_routes_with_different_monitoring_nodes.png'



set yrange [0:12]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Nodes'
set ylabel 'Minumum required length of routes'
set boxwidth 0.5
set style fill solid
# set linetype 1 lc rgb "blue"
plot "barchart_bar_min_length_of_routes_with_different_monitoring_nodes.csv" using 1:2 with boxes notitle


set key left top
set output 'eval_summation_of_all_links_delay_bar_chart.png'
set yrange [:*]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Nodes'
set ylabel 'Summation of All Links Delay (ms)'
set boxwidth 0.5
set style fill solid
# set linetype 1 lc rgb "blue"
# set linetype 2 lc rgb "blue"
plot "barchart_summation_of_all_links_delay_max_len_of_route_all_solved.csv" using 1:2 with boxes notitle


set key left top
set output 'eval_absolute_error_max_len_of_route_all_solved_bar_chart.png'
set yrange [:*]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Nodes'
set ylabel 'Absolute Percent Error'
set boxwidth 0.5
set style fill solid
# set linetype 1 lc rgb "blue"
# set linetype 2 lc rgb "blue"
plot "absolute_error_max_len_of_route_all_solved.csv" using 1:2 with boxes notitle




set terminal png size 2000,768
set key left top
set output 'eval_link_delay_real_and_measured.png'
set yrange [0:*]
set xrange [*:*]
set xlabel 'Link ID'
set ylabel 'Link Delay (ms)'
set boxwidth 0.3
set style fill solid
set style data histograms
plot "abilene_1_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 2:xtic(4) title "Real Delay",\
"abilene_1_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4)  title "Measured Delay - 1 Monitoring Host",\
"abilene_2_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4) title "Measured Delay - 2 Monitoring Host",\
"abilene_3_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4) title "Measured Delay - 3 Monitoring Host",\
"abilene_4_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4)  title "Measured Delay - 4 Monitoring Host",\
"abilene_5_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4) title "Measured Delay - 5 Monitoring Host"




