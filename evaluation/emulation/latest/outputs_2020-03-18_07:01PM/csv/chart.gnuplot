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
plot 'solved_abilene_1.csv' u 4:11 w lp t '1 Monitoring Node', 'solved_abilene_2.csv' u 4:11 w lp t '2 Monitoring Node','solved_abilene_3.csv' u 4:11 w lp t '3 Monitoring Node','solved_abilene_4.csv' u 4:11 w lp t '4 Monitoring Node','solved_abilene_5.csv' u 4:11 w lp t '5 Monitoring Node'


set key right bottom
set output 'eval_Abilene_Max_Length_of_Routes_Links_Monitored.png'
set yrange [0:100]
set xrange [2:15]
set xlabel 'Max Length of Routes'
set ylabel 'Links Monitored (%)'
plot 'all_abilene_1.csv' u 4:8 w lp t '1 Monitoring Node', 'all_abilene_2.csv' u 4:8 w lp t '2 Monitoring Node','all_abilene_3.csv' u 4:8 w lp t '3 Monitoring Node','all_abilene_4.csv' u 4:8 w lp t '4 Monitoring Node','all_abilene_5.csv' u 4:8 w lp t '5 Monitoring Node'



set key top left
set output 'eval_Abilene_Max_Length_of_Routes_Execution_time_ILP.png'
set yrange [0:*]
set xrange [2:15]
set xlabel 'Max Length of Routes'
set ylabel 'Execution Time (ms)'
plot 'all_abilene_1.csv' u 4:3 w lp t '1 Monitoring Node', 'all_abilene_2.csv' u 4:3 w lp t '2 Monitoring Node','all_abilene_3.csv' u 4:3 w lp t '3 Monitoring Node','all_abilene_4.csv' u 4:3 w lp t '4 Monitoring Node','all_abilene_5.csv' u 4:3 w lp t '5 Monitoring Node'



set key top left
set output 'eval_Abilene_Max_Length_of_Routes_Number_of_Required_Rules.png'

set yrange [0:170]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Monitoring Overhead (Number of Rules)'
plot 'solved_abilene_1.csv' u 4:10 w lp t '1 Monitoring Node', 'solved_abilene_2.csv' u 4:10 w lp t '2 Monitoring Node','solved_abilene_3.csv' u 4:10 w lp t '3 Monitoring Node','solved_abilene_4.csv' u 4:10 w lp t '4 Monitoring Node','solved_abilene_5.csv' u 4:10 w lp t '5 Monitoring Node'


set key left top
set output 'eval_Abilene_Max_Length_of_Max_error_per_one_link.png'

set yrange [0:15]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Max Error Per Link (ms)'
plot 'solved_abilene_1.csv' u 4:12 w lp t '1 Monitoring Node', 'solved_abilene_2.csv' u 4:12 w lp t '2 Monitoring Node','solved_abilene_3.csv' u 4:12 w lp t '3 Monitoring Node','solved_abilene_4.csv' u 4:12 w lp t '4 Monitoring Node','solved_abilene_5.csv' u 4:12 w lp t '5 Monitoring Node'


set key left bottom
set output 'eval_Abilene_Max_Length_of_Routes_Execution_time_PSO.png'
set yrange [0:*]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Execution time (s)'
plot 'solved_abilene_1.csv' u 4:($14/1000) w lp t '1 Monitoring Node', 'solved_abilene_2.csv' u 4:($14/1000) w lp t '2 Monitoring Node','solved_abilene_3.csv' u 4:($14/1000) w lp t '3 Monitoring Node','solved_abilene_4.csv' u 4:($14/1000) w lp t '4 Monitoring Node','solved_abilene_5.csv' u 4:($14/1000) w lp t '5 Monitoring Node'






set key left top
set output 'eval_Abilene_Max_Length_of_Summation_of_All_Links_Error.png'
set yrange [0:130]
set xrange [5:15]
set xlabel 'Max Length of Routes'
set ylabel 'Summation of All Link Delays Error (ms)'
plot 'solved_abilene_1.csv' u 4:13 w lp t '1 Monitoring Node', 'solved_abilene_2.csv' u 4:13 w lp t '2 Monitoring Node','solved_abilene_3.csv' u 4:13 w lp t '3 Monitoring Node','solved_abilene_4.csv' u 4:13 w lp t '4 Monitoring Node','solved_abilene_5.csv' u 4:13 w lp t '5 Monitoring Node'


set key left top
set output 'eval_barchart_Average_Percent_of_Rules_to_Switch_Rule_Capacity_Ratio_max_len_of_route_11.png'

set yrange [0:20]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Nodes'
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


# set key left top
# set output 'eval_summation_of_all_links_delay_and_percent_error_bar_chart.png'
# set yrange [:*]
# set xrange [0.5:5.5]
# set xlabel 'Number of Monitoring Nodes'
# set ylabel 'Summation of All Links Delay (ms)'
# set boxwidth 0.5
# set style fill solid

# set y2range [:*]
# set y2tics 0.05
# set y2label 'Absolute Percent Error'
# #set linetype 2 lc rgb "blue"
# plot "barchart_summation_of_all_links_delay_max_len_of_route_all_solved.csv" using 2:xtic(1) with boxes title "Summation of All Links Delay (ms)",\
# "absolute_error_max_len_of_route_all_solved.csv" using 1:2 axes x1y2  w lp title "Absolute Percent Error"
# unset y2label
# unset y2tics


set key left top
set output 'eval_summation_of_all_links_delay_and_percent_error_bar_chart.png'
set yrange [:*]
set xrange [0.5:5.5]
set xlabel 'Number of Monitoring Nodes'
set ylabel 'Summation of All Links Delay (ms)'
set boxwidth 0.5
set style fill solid

#set linetype 1 lc rgb "green"
set y2range [0:100]
set y2tics 10
set y2label 'Absolute Percent Error'
#set linetype 2 lc rgb "blue"
plot "barchart_summation_of_all_links_delay_max_len_of_route_all_solved.csv" using 1:2 with boxes title "Summation of All Links Delay (ms)",\
"absolute_error_max_len_of_route_all_solved.csv" using 1:2 axes x1y2  w lp title "Absolute Percent Error"
unset y2label
unset y2tics



set terminal png size 2000,768
#set key outside
#set key at -10,-10
set key top left horizontal
set key font ",18"
set output 'eval_link_delay_real_and_measured.png'
set yrange [0:*]
set xrange [*:*]
set xlabel 'Link ID'
set xlabel font ",20"
set ylabel 'Link Delay (ms)'
set ylabel font ",20"
set boxwidth 0.35
set style fill solid
set style data histograms
set bmargin 4
set lmargin 10
set xtics font ",15"
set ytics font ",15"


plot "abilene_1_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3  title "Measured Delay - 1 Monitoring Node",\
"abilene_2_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3 title "Measured Delay - 2 Monitoring Node",\
"abilene_3_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3 title "Measured Delay - 3 Monitoring Node",\
"abilene_4_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3  title "Measured Delay - 4 Monitoring Node",\
"abilene_5_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 3:xtic(4) title "Measured Delay - 5 Monitoring Node",\
"abilene_5_barchart_real_and_measured_delay_max_len_of_route_all_solved.csv" using 2 title "Real Delay"