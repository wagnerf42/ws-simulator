#!/bin/bash

    echo "#filename work depth proc a b c"
for i in $*
do
    gnuplot -e "filename='$i'" fitting.gnu 2> log
    var_a=$(grep "a               = " log | cut -d " " -f17)
    var_b=$(grep "b               = " log | cut -d " " -f17)
    var_c=$(grep "c               = " log | cut -d " " -f17)

    first_char=$(sed -n 4p $i | cut -c1-1)

    if [ $first_char = "#" ]
    then
        work=$(sed -n 2p $i | cut -d ":" -f1-3 | cut -d "," -f1 | cut -d ":" -f2)
        depth=$(sed -n 2p $i | cut -d ":" -f1-3 | cut -d "," -f2 | cut -d ":" -f2)
        proc=$(sed -n 9p $i  | cut -d "	" -f6)   #pay attention for the speace between variables
    else
        proc=$(sed -n 9p $i  | cut -d "	" -f6)   #pay attention for the speace between variables
        work=$(sed -n 9p $i  | cut -d "	" -f7)
        depth=0
    fi

    echo $i" "$work" "$depth" "$proc" "$var_a" "$var_b" "$var_c

done
