#! /usr/bin/gnuplot
set term png
set terminal png linewidth 2
set key left top
set output 'eval_Abilene_Max_Length_of_Routes_Execution_time.png'
set grid
set title 'Abilene'
set yrange [0:270]
set xrange [10:28]

set xlabel 'Max Length of Routes'
set ylabel 'Execution Time (ms)'
#set label 'finished walk' at 15, 140
#unset label
#set label 'finished walk' at 15, 105
#plot 'bp-hr.dat' u 1:2 w lp t 'systolic', 'bp-hr.dat' u 1:3 w lp t 'diastolic', 'bp-hr.dat' u 1:4 w lp t 'heartrate'
plot 'all_Abilene_1_hosts.csv' u 4:3 w lp t '1 Monitoring node', 'all_Abilene_2_hosts.csv' u 4:3 w lp t '2 Monitoring nodes','all_Abilene_3_hosts.csv' u 4:3 w lp t '3 Monitoring nodes','all_Abilene_4_hosts.csv' u 4:3 w lp t '4 Monitoring nodes','all_Abilene_5_hosts.csv' u 4:3 w lp t '5 Monitoring nodes'
