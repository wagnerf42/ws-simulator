#!/usr/bin/env gnuplot

set term postscript eps color blacktext "Helvetica" 11
set grid

set output "overhead_diff_latency.eps"

set xlabel 'Probabilities'                                                         
set ylabel 'Overhead SimulTime - W/p'                                             


set title ' Overhead according to rsp with different latencies ( p = 32 ) '

set yrange [0:30000]

p "p32l50" u 1:4 s u w l t "lat=50", "p32l100" u 1:4 s u w l t "lat=100"  , "p32l150" u 1:4 s u w l t "lat=150" , "p32l200" u 1:4 s u w l t "lat=200" , "p32l250" u 1:4 s u w l t "lat=250"


set title ' Overhead according to rsp with different latencies ( p = 64 ) '

p "p64l50" u 1:4 s u w l t "lat=50", "p64l100" u 1:4 s u w l t "lat=100"  , "p64l150" u 1:4 s u w l t "lat=150" , "p64l200" u 1:4 s u w l t "lat=200" , "p64l250" u 1:4 s u w l t "lat=250"


set title ' Overhead according to rsp with different latencies ( p = 128 ) '
p "p128l50" u 1:4 s u w l t "lat=50", "p128l100" u 1:4 s u w l t "lat=100"  , "p128l150" u 1:4 s u w l t "lat=150" , "p128l200" u 1:4 s u w l t "lat=200" , "p128l250" u 1:4 s u w l t "lat=250"

set title ' Overhead according to rsp with different latencies ( p = 256 ) '
p "p256l50" u 1:4 s u w l t "lat=50", "p256l100" u 1:4 s u w l t "lat=100"  , "p256l150" u 1:4 s u w l t "lat=150" , "p256l200" u 1:4 s u w l t "lat=200" , "p256l250" u 1:4 s u w l t "lat=250"


set output "overhead_diff_#Processors.eps"
set yrange [0:30000]

set title ' Overhead according to rsp with different #processors ( latency = 50 ) '
p "p32l50" u 1:4 s u w l t "#proc=32" , "p64l50" u 1:4 s u w l t "#proc=64" , "p128l50" u 1:4 s u w l t "#proc=128" , "p256l50" u 1:4 s u w l t "#proc=256"


set title ' Overhead according to rsp with different #processors ( latency = 100 ) '
 p "p32l100" u 1:4 s u w l t "#proc=32" , "p64l100" u 1:4 s u w l t "#proc=64" , "p128l100" u 1:4 s u w l t "#proc=128" , "p256l100" u 1:4 s u w l t "#proc=256"


set title ' Overhead according to rsp with different #processors ( latency = 150 ) '
 p "p32l150" u 1:4 s u w l t "#proc=32" , "p64l150" u 1:4 s u w l t "#proc=64" , "p128l150" u 1:4 s u w l t "#proc=128" , "p256l150" u 1:4 s u w l t "#proc=256"

set title ' Overhead according to rsp with different #processors ( latency = 200 ) '
 p "p32l200" u 1:4 s u w l t "#proc=32" , "p64l200" u 1:4 s u w l t "#proc=64" , "p128l200" u 1:4 s u w l t "#proc=128" , "p256l200" u 1:4 s u w l t "#proc=256"

set title ' Overhead according to rsp with different #processors ( latency = 250 ) '
 p "p32l250" u 1:4 s u w l t "#proc=32" , "p64l250" u 1:4 s u w l t "#proc=64" , "p128l250" u 1:4 s u w l t "#proc=128" , "p256l250" u 1:4 s u w l t "#proc=256"


unset yrange
set output "Work_On_Clusters.eps"

set multiplot layout 3, 1 title '(latency = 50)' font ",14"
 
set lmargin at screen 0.1
set xtics
unset xlabel 
unset ylabel 
unset title

#set title 'Ratio between Work on P1 and P2 according to rsp with different #processors ( latency = 50 ) '
set yrange [0.95:1.2]       
set ylabel "W0 / W1"
 p "p32l50" u 1:($9/$10) s u w l t "#proc=32" , "p64l50" u 1:($9/$10) s u w l t "#proc=64" , "p128l50" u 1:($9/$10) s u w l t "#proc=128" , "p256l50" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]
p "p32l50" u 1:($7/$8) s u w l t "#proc=32" , "p64l50" u 1:($7/$8) s u w l t "#proc=64" , "p128l50" u 1:($7/$8) s u w l t "#proc=128" , "p256l50" u 1:($7/$8) s u w l t "#proc=256"
set xtics
set xlabel "probabilities"
set yrange [0:10000]       
set ylabel "Overhead"

p "p32l50" u 1:4 s u w l t "#proc=32" , "p64l50" u 1:4 s u w l t "#proc=64" , "p128l50" u 1:4 s u w l t "#proc=128" , "p256l50" u 1:4 s u w l t "#proc=256"

unset multiplot

set title 'Ratio between Work on P1 and P2 according to rsp with different #processors ( latency = 100 ) '
 p "p32l100" u 1:($9/$10) s u w l t "#proc=32" , "p64l100" u 1:($9/$10) s u w l t "#proc=64" , "p128l100" u 1:($9/$10) s u w l t "#proc=128" , "p256l100" u 1:($9/$10) s u w l t "#proc=256"


set title 'Ratio between Work on P1 and P2 according to rsp with different #processors ( latency = 150 ) '
 p "p32l150" u 1:($9/$10) s u w l t "#proc=32" , "p64l150" u 1:($9/$10) s u w l t "#proc=64" , "p128l150" u 1:($9/$10) s u w l t "#proc=128" , "p256l150" u 1:($9/$10) s u w l t "#proc=256"

set title 'Ratio between Work on P1 and P2 according to rsp with different #processors ( latency = 200 ) '
 p "p32l200" u 1:($9/$10) s u w l t "#proc=32" , "p64l200" u 1:($9/$10)  s u w l t "#proc=64" , "p128l200" u 1:($9/$10) s u w l t "#proc=128" , "p256l200" u 1:($9/$10) s u w l t "#proc=256"

set title 'Ratio between Work on P1 and P2 according to rsp with different #processors ( latency = 250 ) '
 p "p32l250" u 1:($9/$10) s u w l t "#proc=32" , "p64l250" u 1:($9/$10)  s u w l t "#proc=64" , "p128l250" u 1:($9/$10) s u w l t "#proc=128" , "p256l250" u 1:($9/$10) s u w l t "#proc=256"


