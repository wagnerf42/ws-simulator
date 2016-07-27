#!/usr/bin/env gnuplot

set term pdf enhanced size 8, 8 
set grid
set key inside 



set output 'plot1.pdf'

set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w10000_l5.data" using 1:2 pt 1 ps 0.25 

set origin 0.0, 0.0
plot "log_p100_w10000_l10.data" u 1:2 pt 2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w10000_l15.data" u 1:2 pt 3 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w10000_l20.data" u 1:2 pt 4 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5 

set origin 0.0, 0.5
plot "log_p100_w10000_l25.data" u 1:2 pt 5 ps 0.25

unset multiplot



set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w20000_l5.data" using 1:2 pt 1 ps 0.25 

set origin 0.0, 0.0
plot "log_p100_w20000_l10.data" u 1:2 pt 2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w20000_l15.data" u 1:2 pt 3 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w20000_l20.data" u 1:2 pt 4 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5  

set origin 0.0, 0.5
plot "log_p100_w20000_l25.data" u 1:2 pt 5 ps 0.25

unset multiplot


set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w30000_l5.data" using 1:2 pt 1 ps 0.25 

set origin 0.0, 0.0
plot "log_p100_w30000_l10.data" u 1:2 pt 2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w30000_l15.data" u 1:2 pt 3 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w30000_l20.data" u 1:2 pt 4 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w30000_l25.data" u 1:2 pt 5 ps 0.25

unset multiplot

set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w40000_l5.data" using 1:2 pt 1 ps 0.25 

set origin 0.0, 0.0
plot "log_p100_w40000_l10.data" u 1:2 pt 2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w40000_l15.data" u 1:2 pt 3 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w40000_l20.data" u 1:2 pt 4 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w40000_l25.data" u 1:2 pt 5 ps 0.25

unset multiplot


set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w50000_l5.data" using 1:2 pt 1 ps 0.25 

set origin 0.0, 0.0
plot "log_p100_w50000_l10.data" u 1:2 pt 2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w50000_l15.data" u 1:2 pt 3 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w50000_l20.data" u 1:2 pt 4 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w50000_l25.data" u 1:2 pt 5 ps 0.25

unset multiplot


# varier Work avec latence constante
set output 'plot2.pdf'

set multiplot
set size 1, 0.5 

set origin 0.0, 0.5 
plot "log_p100_w10000_l5.data" using 1:2 ps 0.25, "log_p100_w20000_l5.data" u 1:2 ps 0.25, "log_p100_w30000_l5.data" u 1:2 ps 0.25, "log_p100_w40000_l5.data" u 1:2 ps 0.25, "log_p100_w50000_l5.data" u 1:2 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w10000_l10.data" using 1:2 ps 0.25, "log_p100_w20000_l10.data" u 1:2 ps 0.25, "log_p100_w30000_l10.data" u 1:2 ps 0.25, "log_p100_w40000_l10.data" u 1:2 ps 0.25, "log_p100_w50000_l10.data" u 1:2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5

set origin 0.0, 0.5
plot "log_p100_w10000_l15.data" using 1:2 ps 0.25, "log_p100_w20000_l15.data" u 1:2 ps 0.25, "log_p100_w30000_l15.data" u 1:2 ps 0.25, "log_p100_w40000_l15.data" u 1:2 ps 0.25, "log_p100_w50000_l15.data" u 1:2 ps 0.25

set origin 0.0, 0.0
plot "log_p100_w10000_l20.data" using 1:2 ps 0.25, "log_p100_w20000_l20.data" u 1:2 ps 0.25, "log_p100_w30000_l20.data" u 1:2 ps 0.25, "log_p100_w40000_l20.data" u 1:2 ps 0.25, "log_p100_w50000_l20.data" u 1:2 ps 0.25

unset multiplot                                                                
                                                                                
set multiplot                                                                  
set size 1, 0.5 

set origin 0.0, 0.5
plot "log_p100_w10000_l25.data" using 1:2 ps 0.25, "log_p100_w20000_l25.data" u 1:2 ps 0.25, "log_p100_w30000_l25.data" u 1:2 ps 0.25, "log_p100_w40000_l25.data" u 1:2 ps 0.25, "log_p100_w50000_l25.data" u 1:2 ps 0.25

unset multiplot


