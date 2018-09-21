#!/usr/bin/env gnuplot


set term postscript eps color blacktext "Helvetica" 12
set grid
set xlabel 'Latency'
set ylabel 'Overhead'


set output "tasks.eps"  
p "tasks_100000000_128.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=128 ", (12864.8)*x + (-740.491)*x*log(x) + (-10034) 
p "tasks_100000000_16.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=16 ", (1039)*x + (-53.077)*x*log(x) + (1815.34) 
p "tasks_100000000_256.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=256 ", (26395.2)*x + (-1451.23)*x*log(x) + (14828.7) 
p "tasks_100000000_32.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=32 ", (2442.9)*x + (-122.659)*x*log(x) + (6481.79) 
p "tasks_100000000_64.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=64 ", (5844.59)*x + (-327.588)*x*log(x) + (-814.797) 
p "tasks_100000000_8.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=8 ", (378.669)*x + (-19.4782)*x*log(x) + (-29.2717) 
p "tasks_10000000_128.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=128 ", (11545.8)*x + (-798.517)*x*log(x) + (-13616.2) 
p "tasks_10000000_16.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=16 ", (957.368)*x + (-61.0685)*x*log(x) + (-381.727) 
p "tasks_10000000_256.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=256 ", (23415.7)*x + (-1544.58)*x*log(x) + (2044.35) 
p "tasks_10000000_32.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=32 ", (2300.36)*x + (-150.06)*x*log(x) + (-93.2203) 
p "tasks_10000000_64.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=64 ", (5042.45)*x + (-323.378)*x*log(x) + (1590.35) 
p "tasks_10000000_8.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=8 ", (329.383)*x + (-19.122)*x*log(x) + (71.5242) 
p "tasks_100000000_128.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=128 ", (12864.8)*x + (-740.491)*x*log(x) 
p "tasks_100000000_16.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=16 ", (1039)*x + (-53.077)*x*log(x) 
p "tasks_100000000_256.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=256 ", (26395.2)*x + (-1451.23)*x*log(x) 
p "tasks_100000000_32.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=32 ", (2442.9)*x + (-122.659)*x*log(x) 
p "tasks_100000000_64.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=64 ", (5844.59)*x + (-327.588)*x*log(x) 
p "tasks_100000000_8.data" u 2:($5*$6-$7) w lp title " w=100000000 depth=0 p=8 ", (378.669)*x + (-19.4782)*x*log(x) 
p "tasks_10000000_128.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=128 ", (11545.8)*x + (-798.517)*x*log(x) 
p "tasks_10000000_16.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=16 ", (957.368)*x + (-61.0685)*x*log(x) 
p "tasks_10000000_256.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=256 ", (23415.7)*x + (-1544.58)*x*log(x) 
p "tasks_10000000_32.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=32 ", (2300.36)*x + (-150.06)*x*log(x) 
p "tasks_10000000_64.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=64 ", (5042.45)*x + (-323.378)*x*log(x) 
p "tasks_10000000_8.data" u 2:($5*$6-$7) w lp title " w=10000000 depth=0 p=8 ", (329.383)*x + (-19.122)*x*log(x) 
