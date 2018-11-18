#!/usr/bin/env gnuplot


#set terminal pdf
set terminal postscript eps enhanced color font 'Helvetica,10'

set grid
set xlabel 'Initial block'
set ylabel 'run_time'


#p "block_fix" u 2:5

#set ylabel 'waiting_time'


#p "block_fix" u 2:6

unset yrange#[0:1000]
unset xrange#[0:100000]

set output "diff_blks_stop.eps"

p "blk_factor_2-iws-100_000-p_4" u 10:5 s u w l, "blk_factor_2-iws-100_000-p_4_3" u 10:5 s u w l, "blk_factor_2-iws-100_000-p_4_5" u 10:5 s u w l, "blk_factor_2-iws-100_000-p_4_7" u 10:5 s u w l,


f(k, n , b, c) = k*c + b*2**k
g(k, n , b, c) = (n - b*2**(k+1) + b) * c / k + k*c
h(k, n , b, c) = f(k, n , b, c) + g(k, n , b, c)

n = 10000000
b = n / 1000
c = 10


#p f(x, n , b, c) , g(x, n , b, c), h(k, n , b, c)
