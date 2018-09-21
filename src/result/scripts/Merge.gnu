#!/usr/bin/env gnuplot


set term postscript eps color blacktext "Helvetica" 12
set grid
set xlabel 'Latency'
set ylabel 'Overhead'


set output "Merge.eps"  
p "Merge_Sort_2_128.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=128 ", (26752.8)*x + (-1904.1)*x*log(x) + (2.51389e+07) 
p "Merge_Sort_2_16.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=16 ", (3746.68)*x + (-299.052)*x*log(x) + (1.43061e+06) 
p "Merge_Sort_2_32.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=32 ", (7918.01)*x + (-621.441)*x*log(x) + (3.93404e+06) 
p "Merge_Sort_2_4.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=4 ", (182.018)*x + (-6.27758)*x*log(x) + (220258) 
p "Merge_Sort_2_64.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=64 ", (18764)*x + (-1535.16)*x*log(x) + (8.60109e+06) 
p "Merge_Sort_2_8.data" u 2:($5*$6-$7) s u w lp title " w=9321255 depth=282845 p=8 ", (1333.46)*x + (-99.2792)*x*log(x) + (517757) 
p "Merge_Sort_4_128.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=128 ", (23158.1)*x + (-1662.65)*x*log(x) + (9.57831e+07) 
p "Merge_Sort_4_16.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=16 ", (6897.02)*x + (-634.965)*x*log(x) + (3.91048e+06) 
p "Merge_Sort_4_32.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=32 ", (8687.17)*x + (-725.222)*x*log(x) + (1.65691e+07) 
p "Merge_Sort_4_4.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=4 ", (515.157)*x + (-39.4097)*x*log(x) + (280642) 
p "Merge_Sort_4_64.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=64 ", (11535)*x + (-816.651)*x*log(x) + (4.28584e+07) 
p "Merge_Sort_4_8.data" u 2:($5*$6-$7) s u w lp title " w=10581248 depth=844030 p=8 ", (2721.2)*x + (-242.668)*x*log(x) + (611582) 
p "Merge_Sort_6_128.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=128 ", (18251.5)*x + (-1079.33)*x*log(x) + (4.41023e+07) 
p "Merge_Sort_6_16.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=16 ", (3954.06)*x + (-319.836)*x*log(x) + (2.24336e+06) 
p "Merge_Sort_6_32.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=32 ", (7486.43)*x + (-585.124)*x*log(x) + (6.93119e+06) 
p "Merge_Sort_6_4.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=4 ", (246.322)*x + (-13.4616)*x*log(x) + (326070) 
p "Merge_Sort_6_64.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=64 ", (14267.9)*x + (-1079.66)*x*log(x) + (1.69239e+07) 
p "Merge_Sort_6_8.data" u 2:($5*$6-$7) s u w lp title " w=10088973 depth=432675 p=8 ", (1497.81)*x + (-117.515)*x*log(x) + (819043) 
p "Merge_Sort_8_128.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=128 ", (16528.3)*x + (-845.001)*x*log(x) + (4.52056e+07) 
p "Merge_Sort_8_16.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=16 ", (4076.5)*x + (-330.459)*x*log(x) + (2.5618e+06) 
p "Merge_Sort_8_32.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=32 ", (8169.7)*x + (-647.054)*x*log(x) + (6.85598e+06) 
p "Merge_Sort_8_4.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=4 ", (213.068)*x + (-11.5312)*x*log(x) + (480558) 
p "Merge_Sort_8_64.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=64 ", (13146.4)*x + (-933.623)*x*log(x) + (1.74927e+07) 
p "Merge_Sort_8_8.data" u 2:($5*$6-$7) s u w lp title " w=10159328 depth=444825 p=8 ", (1631.72)*x + (-132.367)*x*log(x) + (1.04696e+06) 
