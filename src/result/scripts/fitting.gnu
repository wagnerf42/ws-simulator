#!/usr/bin/env gnuplot


#f(x) = a*x*log(x) +b*log(x) + c*x
f(x) =  a*x + b*x*log(x) + c

#fit f(x)  "merge_sort_4_128.data" u 2:($5*$6-$7) via a,b,c

fit f(x) filename u 2:($5*$6-$7) via a,b,c 
