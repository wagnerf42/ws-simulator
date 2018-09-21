#!/bin/bash

latency=$1

echo $latency

echo "#prb Latency RunTime Overhead ISR ESR IDATAT EDATAT W0 W1" > p32l$latency 
awk -F ' ' '{ if($2=='$latency') print $1 " " $2 " "  $5 " " ($5 - $7/$6)  " " $3 " " $4 " " $11 " " $12 " " $13 " " $14  }' p32 >> p32l$latency
echo "p32l"$latency 

echo "#prb Latency RunTime Overhead ISR ESR IDATAT EDATAT W0 W1" > p64l$latency 
awk -F ' ' '{ if($2=='$latency') print $1 " " $2 " "  $5 " " ($5 - $7/$6)  " " $3 " " $4 " " $11 " " $12 " " $13 " " $14   }' p64 >> p64l$latency
echo "p64l"$latency 


echo "#prb Latency RunTime Overhead ISR ESR IDATAT EDATAT W0 W1" > p128l$latency 
awk -F ' ' '{ if($2=='$latency') print $1 " " $2 " "  $5 " " ($5 - $7/$6) " " $3 " " $4 " " $11 " " $12 " " $13 " " $14  }' p128 >> p128l$latency
echo "p128l"$latency 

echo "#prb Latency RunTime Overhead ISR ESR IDATAT EDATAT W0 W1" > p256l$latency 
awk -F ' ' '{ if($2=='$latency') print $1 " " $2 " "  $5 " " ($5 - $7/$6) " " $3 " " $4 " " $11 " " $12 " " $13 " " $14  }' p256 >> p256l$latency
echo "p256l"$latency 


