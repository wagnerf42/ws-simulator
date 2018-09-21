#!/usr/bin/env gnuplot


set term postscript eps color blacktext "Helvetica" 12
set grid
set xlabel 'Latency'
set ylabel 'Overhead'


set output "load.eps"  
p "load_100000000_128.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=128 ", (12833.4)*x + (-737.383)*x*log(x) + (-18450.8) 
p "load_100000000_16.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=16 ", (1178.4)*x + (-69.8262)*x*log(x) + (-22383.2) 
p "load_100000000_32.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=32 ", (2444.01)*x + (-127.225)*x*log(x) + (29702.3) 
p "load_100000000_4.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=4 ", (57.6346)*x + (-2.36158)*x*log(x) + (-27.7673) 
p "load_100000000_64.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=64 ", (5640.13)*x + (-306.951)*x*log(x) + (60024.4) 
p "load_100000000_8.data" u 2:($5*$6-$7) s u w lp title " w=100000000 depth=0 p=8 ", (412.261)*x + (-23.2741)*x*log(x) + (-6395.11) 
p "load_10000000_128.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=128 ", (11377.3)*x + (-767.854)*x*log(x) + (-10108.8) 
p "load_10000000_16.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=16 ", (964.704)*x + (-61.6029)*x*log(x) + (-1997.9) 
p "load_10000000_32.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=32 ", (2313.2)*x + (-151.254)*x*log(x) + (1769.51) 
p "load_10000000_4.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=4 ", (42.5475)*x + (-0.95815)*x*log(x) + (13.2952) 
p "load_10000000_64.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=64 ", (5425)*x + (-370.209)*x*log(x) + (-39460) 
p "load_10000000_8.data" u 2:($5*$6-$7) s u w lp title " w=10000000 depth=0 p=8 ", (345.717)*x + (-21.1721)*x*log(x) + (-873.451) 
