#!/bin/bash

echo "./simulator.py -p 4 -iws 1000 -l 10"
#./simulator.py -p 4 -iws 1000 -l 10

echo "./simulator.py -p 4 -iws 1000 -l 10 -r 3 "
#./simulator.py -p 4 -iws 1000 -l 10 -r 3

echo "./simulator.py -p 4 -iwsconf 100 1000 10 -l 3 -r 3 "
#./simulator.py -p 4 -iwsconf 100 1000 10 -l 3 -r 3

echo " ./simulator.py -p 4 -tasks -tt 10 -iws 1000 -l 10 "
#./simulator.py -p 4 -tasks -tt 10 -iws 1000 -l 10

echo " ./simulator.py -p 4 -tasks -tt 10 -iws 1000 -l 10 -r 3 "
#./simulator.py -p 4 -tasks -tt 10 -iws 1000 -l 10 -r 3

echo " ./simulator.py -p 4 -tasks -tt 10 -iwsconf 100 1000 10 -l 3 -r 3 "
#./simulator.py -p 4 -tasks -tt 10 -iwsconf 100 1000 10 -l 3 -r 3


echo " ./simulator.py -p 4 -json_in tasks_file/merge_sort_2.json -l 10  "
#./simulator.py -p 4 -json_in tasks_file/merge_sort_2.json -l 10

echo " ./simulator.py -p 4 -json_in tasks_file/merge_sort_2.json -l 10 -r 3 "
#./simulator.py -p 4 -json_in tasks_file/merge_sort_2.json -l 10 -r 3

echo " ./simulator.py -p 4 -adapt -iws 1000 -l 10  "
#./simulator.py -p 4 -adapt -l 10

echo " ./simulator.py -p 4 -adapt -iws 1000 -l 10 -r 3  "
#./simulator.py -p 4 -adapt -l 10 -r 3




