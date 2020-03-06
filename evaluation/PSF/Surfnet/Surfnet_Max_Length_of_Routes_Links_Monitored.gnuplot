#! /usr/bin/gnuplot
set term png
set terminal png linewidth 2
set key right bottom
set output 'eval_Surfnet_Max_Length_of_Routes_Links_Monitored.png'
set grid
#set title 'Abilene topology with different percent of TG Agents/switch ratio'
set yrange [1:100]
set xrange [2:14]
#set format x "%.6f"
set xlabel 'Max Length of Routes'
set ylabel 'Links Monitored (%)'
#set label 'finished walk' at 15, 140
#unset label
#set label 'finished walk' at 15, 105
#plot 'bp-hr.dat' u 1:2 w lp t 'systolic', 'bp-hr.dat' u 1:3 w lp t 'diastolic', 'bp-hr.dat' u 1:4 w lp t 'heartrate'
plot 'all_Surfnet_5.csv' u 4:8 w lp t '1 Monitoring node (RMS=5%)', 'all_Surfnet_10.csv' u 4:8 w lp t '2 Monitoring node (RMS=10%)','all_Surfnet_20.csv' u 4:8 w lp t '2 Monitoring node (RMS=20%)','all_Surfnet_30.csv' u 4:8 w lp t '3 Monitoring node (RMS=30%)'