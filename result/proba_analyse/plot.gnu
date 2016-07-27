#!/usr/bin/env gnuplot

set term pdf enhanced size 8, 8 
set grid
set key inside 


set ytics 100
set yrange [200:]

set output 'plot1.pdf'

set multiplot
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l1.data" u 1:2 t 'Latency = 1' pt 2 ps 0.5

set origin 0.0, 0.0
plot "log_p100_w20000_l5.data" u 1:2 t 'Latency = 5' pt 2 ps 0.5
unset multiplot



set multiplot
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l10.data" u 1:2 t 'Latency = 10' pt 2 ps 0.5

set origin 0.0, 0.0
plot "log_p100_w20000_l15.data" u 1:2 t 'Latency = 15' pt 2 ps 0.5
unset multiplot

set multiplot
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l20.data" u 1:2 t 'Latency = 20' pt 2 ps 0.5

set origin 0.0, 0.0
plot "log_p100_w20000_l15.data" u 1:2 t 'Latency = 25' pt 2 ps 0.5
unset multiplot

set multiplot
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l30.data" u 1:2 t 'Latency = 30' pt 2 ps 0.5

set origin 0.0, 0.0
plot "log_p100_w20000_l40.data" u 1:2 t 'Latency = 40' pt 2 ps 0.5
unset multiplot

set multiplot
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l50.data" u 1:2 t 'Latency = 50' pt 2 ps 0.5



unset multiplot

