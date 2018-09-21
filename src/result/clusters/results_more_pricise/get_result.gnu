#!/usr/bin/env gnuplot

#set term postscript eps color blacktext "Helvetica" 11
set terminal pdf color font "Helvetica, 9"
set grid

set output "overhead_ratio.pdf"

set xrange [0:1]
set yrange [0:14000]       
unset yrange

set multiplot layout 3, 1 title '(latency = 2)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"


p "p32l2" u 1:($9/$10) s u w l t "#proc=32" , "p64l2" u 1:($9/$10) s u w l t "#proc=64" , "p128l2" u 1:($9/$10) s u w l t "#proc=128" , "p256l2" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l2" u 1:($7/$8) s u w l t "#proc=32" , "p64l2" u 1:($7/$8) s u w l t "#proc=64" , "p128l2" u 1:($7/$8) s u w l t "#proc=128" , "p256l2" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l2" u 1:4 s u w l t "#proc=32" , "p64l2" u 1:4 s u w l t "#proc=64" , "p128l2" u 1:4 s u w l t "#proc=128" , "p256l2" u 1:4 s u w l t "#proc=256"

unset multiplot


set multiplot layout 3, 1 title '(latency = 6)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"


p "p32l6" u 1:($9/$10) s u w l t "#proc=32" , "p64l6" u 1:($9/$10) s u w l t "#proc=64" , "p128l6" u 1:($9/$10) s u w l t "#proc=128" , "p256l6" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l6" u 1:($7/$8) s u w l t "#proc=32" , "p64l6" u 1:($7/$8) s u w l t "#proc=64" , "p128l6" u 1:($7/$8) s u w l t "#proc=128" , "p256l6" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l6" u 1:4 s u w l t "#proc=32" , "p64l6" u 1:4 s u w l t "#proc=64" , "p128l6" u 1:4 s u w l t "#proc=128" , "p256l6" u 1:4 s u w l t "#proc=256"

unset multiplot

set multiplot layout 3, 1 title '(latency = 10)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"


p "p32l10" u 1:($9/$10) s u w l t "#proc=32" , "p64l10" u 1:($9/$10) s u w l t "#proc=64" , "p128l10" u 1:($9/$10) s u w l t "#proc=128" , "p256l10" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l10" u 1:($7/$8) s u w l t "#proc=32" , "p64l10" u 1:($7/$8) s u w l t "#proc=64" , "p128l10" u 1:($7/$8) s u w l t "#proc=128" , "p256l10" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l10" u 1:4 s u w l t "#proc=32" , "p64l10" u 1:4 s u w l t "#proc=64" , "p128l10" u 1:4 s u w l t "#proc=128" , "p256l10" u 1:4 s u w l t "#proc=256"

unset multiplot



set multiplot layout 3, 1 title '(latency = 26)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"


p "p32l26" u 1:($9/$10) s u w l t "#proc=32" , "p64l26" u 1:($9/$10) s u w l t "#proc=64" , "p128l26" u 1:($9/$10) s u w l t "#proc=128" , "p256l26" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l26" u 1:($7/$8) s u w l t "#proc=32" , "p64l26" u 1:($7/$8) s u w l t "#proc=64" , "p128l26" u 1:($7/$8) s u w l t "#proc=128" , "p256l26" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l26" u 1:4 s u w l t "#proc=32" , "p64l26" u 1:4 s u w l t "#proc=64" , "p128l26" u 1:4 s u w l t "#proc=128" , "p256l26" u 1:4 s u w l t "#proc=256"

unset multiplot

set multiplot layout 3, 1 title '(latency = 38)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"


p "p32l38" u 1:($9/$10) s u w l t "#proc=32" , "p64l38" u 1:($9/$10) s u w l t "#proc=64" , "p128l38" u 1:($9/$10) s u w l t "#proc=128" , "p256l38" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l38" u 1:($7/$8) s u w l t "#proc=32" , "p64l38" u 1:($7/$8) s u w l t "#proc=64" , "p128l38" u 1:($7/$8) s u w l t "#proc=128" , "p256l38" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l38" u 1:4 s u w l t "#proc=32" , "p64l38" u 1:4 s u w l t "#proc=64" , "p128l38" u 1:4 s u w l t "#proc=128" , "p256l38" u 1:4 s u w l t "#proc=256"

unset multiplot


set multiplot layout 3, 1 title '(latency = 50)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel
set yrange [0.95:1.2]
set ylabel "W0 / W1"





p "p32l50" u 1:($9/$10) s u w l t "#proc=32" , "p64l50" u 1:($9/$10) s u w l t "#proc=64" , "p128l50" u 1:($9/$10) s u w l t "#proc=128" , "p256l50" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l50" u 1:($7/$8) s u w l t "#proc=32" , "p64l50" u 1:($7/$8) s u w l t "#proc=64" , "p128l50" u 1:($7/$8) s u w l t "#proc=128" , "p256l50" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:4000]       
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l50" u 1:4 s u w l t "#proc=32" , "p64l50" u 1:4 s u w l t "#proc=64" , "p128l50" u 1:4 s u w l t "#proc=128" , "p256l50" u 1:4 s u w l t "#proc=256"

unset multiplot



set multiplot layout 3, 1 title '(latency = 100)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel 
set yrange [0.95:1.2]       
set ylabel "W0 / W1"

p "p32l100" u 1:($9/$10) s u w l t "#proc=32" , "p64l100" u 1:($9/$10) s u w l t "#proc=64" , "p128l100" u 1:($9/$10) s u w l t "#proc=128" , "p256l100" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l100" u 1:($7/$8) s u w l t "#proc=32" , "p64l100" u 1:($7/$8) s u w l t "#proc=64" , "p128l100" u 1:($7/$8) s u w l t "#proc=128" , "p256l100" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:8000]       
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l100" u 1:4 s u w l t "#proc=32" , "p64l100" u 1:4 s u w l t "#proc=64" , "p128l100" u 1:4 s u w l t "#proc=128" , "p256l100" u 1:4 s u w l t "#proc=256"

unset multiplot





set multiplot layout 3, 1 title '(latency = 150)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel 
set yrange [0.95:1.2]       
set ylabel "W0 / W1"

p "p32l150" u 1:($9/$10) s u w l t "#proc=32" , "p64l150" u 1:($9/$10) s u w l t "#proc=64" , "p128l150" u 1:($9/$10) s u w l t "#proc=128" , "p256l150" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l150" u 1:($7/$8) s u w l t "#proc=32" , "p64l150" u 1:($7/$8) s u w l t "#proc=64" , "p128l150" u 1:($7/$8) s u w l t "#proc=128" , "p256l150" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:10000]       
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l150" u 1:4 s u w l t "#proc=32" , "p64l150" u 1:4 s u w l t "#proc=64" , "p128l150" u 1:4 s u w l t "#proc=128" , "p256l150" u 1:4 s u w l t "#proc=256"

unset multiplot



set multiplot layout 3, 1 title '(latency = 200)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel 
set yrange [0.95:1.2]       
set ylabel "W0 / W1"

p "p32l200" u 1:($9/$10) s u w l t "#proc=32" , "p64l200" u 1:($9/$10) s u w l t "#proc=64" , "p128l200" u 1:($9/$10) s u w l t "#proc=128" , "p256l200" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l200" u 1:($7/$8) s u w l t "#proc=32" , "p64l200" u 1:($7/$8) s u w l t "#proc=64" , "p128l200" u 1:($7/$8) s u w l t "#proc=128" , "p256l200" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:12500]       
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l200" u 1:4 s u w l t "#proc=32" , "p64l200" u 1:4 s u w l t "#proc=64" , "p128l200" u 1:4 s u w l t "#proc=128" , "p256l200" u 1:4 s u w l t "#proc=256"

unset multiplot



set multiplot layout 3, 1 title '(latency = 250)' font ",14"
set lmargin at screen 0.1
set xtics
unset xlabel 
set yrange [0.95:1.2]       
set ylabel "W0 / W1"

p "p32l250" u 1:($9/$10) s u w l t "#proc=32" , "p64l250" u 1:($9/$10) s u w l t "#proc=64" , "p128l250" u 1:($9/$10) s u w l t "#proc=128" , "p256l250" u 1:($9/$10) s u w l t "#proc=256"

unset key
set ylabel "IDATAT / EDATAT"
set yrange[0:16]

p "p32l250" u 1:($7/$8) s u w l t "#proc=32" , "p64l250" u 1:($7/$8) s u w l t "#proc=64" , "p128l250" u 1:($7/$8) s u w l t "#proc=128" , "p256l250" u 1:($7/$8) s u w l t "#proc=256"

set xtics
set xlabel "probabilities"
#set yrange [0:14000]       
set yrange [0:14000]       
set ylabel "Overhead"

p "p32l250" u 1:4 s u w l t "#proc=32" , "p64l250" u 1:4 s u w l t "#proc=64" , "p128l250" u 1:4 s u w l t "#proc=128" , "p256l250" u 1:4 s u w l t "#proc=256"

unset multiplot


















