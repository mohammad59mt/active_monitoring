#! /usr/bin/gnuplot
set term png
set terminal png linewidth 2
set key right bottom
set output 'eval_Abilene_Links_Monitored_execution_time.png'
set grid
#set title 'Abilene topology with different percent of TG Agents/switch ratio'
set yrange [0:100]
set xrange [2:10]
set xlabel 'Max Length of Routes'
set ylabel 'Links Monitored (%)'
#set label 'finished walk' at 15, 140
#unset label
#set label 'finished walk' at 15, 105
#plot 'bp-hr.dat' u 1:2 w lp t 'systolic', 'bp-hr.dat' u 1:3 w lp t 'diastolic', 'bp-hr.dat' u 1:4 w lp t 'heartrate'
plot 'all_Abilene_10.csv' u 4:8 w lp t 'Abilene 10% of hosts', 'all_Abilene_20.csv' u 4:8 w lp t 'Abilene 20% of hosts','all_Abilene_30.csv' u 4:8 w lp t 'Abilene 30% of hosts'