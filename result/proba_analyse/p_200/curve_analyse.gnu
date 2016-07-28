#!/usr/bin/env gnuplot

set term pdf enhanced size 8, 8 
unset xrange
unset yrange

set output 'plot1.pdf'

log2(n) = log(n)/log(2)


temps(proc, work, latency, proba, const1, const2) = work/proc + const1*log2(work)*(proba*latency**0.12) + const2*log2(work)*(1-proba) + 0.94*log2(proc)/(proba)

plot "average_time_p200_w20000000_l5.data" u 1:2, [pr=0.0125:0.5] temps(200, 20000000, 5, pr, 13, 2)

plot "average_time_p200_w20000000_l10.data" u 1:2, [pr=0.0125:0.5] temps(200, 20000000, 10, pr, 13, 2)

plot "average_time_p200_w20000000_l15.data" u 1:2, [pr=0.0125:0.5] temps(200, 20000000, 15, pr, 13, 2)

plot "average_time_p200_w20000000_l20.data" u 1:2, [pr=0.0125:0.5] temps(200, 20000000, 20, pr, 13, 2)

plot "average_time_p200_w20000000_l25.data" u 1:2, [pr=0.0125:0.5] temps(200, 20000000, 25, pr, 13, 2)
