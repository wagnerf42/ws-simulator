#!/bin/bash

file_name=`echo $1| cut -d "_" -f1`


./script.sh $* > $file_name".fit"

cat head_plot  > $file_name".gnu"

echo "set output \""$file_name".eps\"  " >> $file_name".gnu"

awk -F ' ' '{ if (NR!="1") print "p \"" $1 "\" u 2:($5*$6-$7) s u w lp title \" w=" $2 " depth="$3 " p="$4 " \", ("$5")*x + ("$6")*x*log(x) + ("$7") "}' $file_name".fit" >> $file_name".gnu"

#awk -F ' ' '{ if (NR!="1") print "p \"" $1 "\" u 2:($5*$6-$7) w lp title \" w=" $2 " depth="$3 " p="$4 " \", ("$5")*x + ("$6")*x*log(x) + ("$7") "}' $file_name".fit" >> $file_name".gnu"


gnuplot $file_name".gnu"

echo "lancer : evince " $file_name".eps"

evince $file_name".eps"
