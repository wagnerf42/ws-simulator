#!/bin/bash

#./simulator.py -p 32 -iwsconf 20000000 400000000 3  #-rspconf 0.001 0.01 0.001 -lconf 100 10000 500 -r 50 > proc_32
#./simulator.py -p 32 -iwsconf 20000000 400000000 2  -rspconf 0.01 0.1 0.01 -lconf 100 10000 500 -r 50 >> proc_32
#./simulator.py -p 32 -iwsconf 20000000 400000000 2  -rspconf 0.1 0.51 0.05 -lconf 100 10000 500 -r 50 >> proc_32
#./simulator.py -p 32 -iwsconf 20000000 400000000 2  -rspconf 1 1.01 0.05 -lconf 100 10000 500 -r 50 >> proc_32_


for p in {16,32};
do
    for w in {10000000} #,50000000,100000000,500000000}
    do
        for latence in {64}  #{8,16,32,64,128,256,512,1024}
        do
            echo "$latence -> vss_proba_$p\_$w"
            ./simulator.py -p $p -c 2 -iws $w -l $latence -rspconf 0.001 0.02 0.002 -vss 0 -r 100 >> resultat_finition/new_vss_proba\_$p\_$w\_finition
        done
    done
done

