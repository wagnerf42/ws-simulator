#!/bin/bash

size=1000000

init_cost=4
sizeC=$(($size*$init_cost))
rac=$(echo "scale=0; sqrt($(($size*$init_cost)))" | bc -l)
echo "sqrt(size*init_cost : " $rac


for p in {3,5};
do
    for ((min=1; min<=10 ; min++))   ;
    do
        for ((max=$size; max>=100 ; max=$max/10));
        do
            echo $min _ $max
            ./simulator.py -iws 1000000 -p $p -adapt -itc $init_cost -config_type 4 -r 10 -mbs $max -ibs $min >> MIN_MAX_P$p\_W$size\_ITC$sizeC ;
        done;
    done;

    for ((min=10; min<=100 ; min=$min+10))  ;
    do
        for ((max=$size; max>=100 ; max=$max/10));
        do
            echo $min _ $max
#            ./simulator.py -iwsconf 1000000 100000000 10 -p $p -adapt -itc $itc -config_type $conf_type -r 20 > CT$conf_type\_P$p\_ITC$itc ;
            ./simulator.py -iws 1000000 -p $p -adapt -itc $init_cost -config_type 4 -r 10 -mbs $max -ibs $min >> MIN_MAX_P$p\_W$size\_ITC$sizeC ;
        done;
    done;

    for ((min=100; min<=$rac ; min=$min+200))  ;
    do
        for ((max=$size; max>=$min ; max=$max/10));
        do
            echo $min _ $max
#            ./simulator.py -iwsconf 1000000 100000000 10 -p $p -adapt -itc $itc -config_type $conf_type -r 20 > CT$conf_type\_P$p\_ITC$itc ;
            ./simulator.py -iws 1000000 -p $p -adapt -itc $init_cost -config_type 4 -r 10 -mbs $max -ibs $min >> MIN_MAX_P$p\_W$size\_ITC$sizeC ;
        done;
    done;

done




