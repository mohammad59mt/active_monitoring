#! /usr/bin/gnuplot
set term png
set terminal png linewidth 2
set key left top

set output 'eval_Geant_Max_Length_of_Routes_Execution_time.png'
set grid
set title 'Geant'
set yrange [0:1200000]
set xrange [2:7]
set xlabel 'Max Length of Routes'
set ylabel 'Execution Time (ms)'
#set label 'finished walk' at 15, 140
#unset label
#set label 'finished walk' at 15, 105
#plot 'bp-hr.dat' u 1:2 w lp t 'systolic', 'bp-hr.dat' u 1:3 w lp t 'diastolic', 'bp-hr.dat' u 1:4 w lp t 'heartrate'
plot 'all_Geant2012_5.csv' u 4:3 w lp t '1 Monitoring node (RMS=5%)', 'all_Geant2012_10.csv' u 4:3 w lp t '2 Monitoring node (RMS=10%)','all_Geant2012_20.csv' u 4:3 w lp t '2 Monitoring node (RMS=20%)','all_Geant2012_30.csv' u 4:3 w lp t '3 Monitoring node (RMS=30%)'
#'all_Geant2012_20.csv' u 4:3 w lp t '3 Monitoring node (RMS=20%)',