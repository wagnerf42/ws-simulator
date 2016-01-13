#!/usr/bin/env perl

use strict;
use warnings;


die "please give processors number " unless $ARGV[0]=~/^\d+$/;

my $processors_number = $ARGV[0];
my $name = "M_blocs_file";
my @matrix_size_values = (3000);
my @bloc_size_values = (1500, 1000, 750, 600, 500, 375, 300, 250, 200, 150, 120, 100, 75, 60, 50, 40, 30);
#my @bloc_size_values = (3000, 2000, 1500, 1200, 1000, 750, 600, 500, 400, 375, 300, 250, 240, 200, 150, 120, 100, 80, 75, 60, 50);
#my @bloc_size_values = (500, 250, 200, 125, 100, 50, 40, 20, 10);


#my $matrix_size = 6000;
#my $bloc_size = 1500;
print "processor M_size B_size W D T_attendu T_simul \n";
for my $processor (5,7,14){
for my $matrix_size (@matrix_size_values){
	for my $bloc_size (@bloc_size_values){
		
		#while($matrix_size % $bloc_size != 0 ) {
		#	$bloc_size ++ ;
		#}		
	print "$processor $matrix_size $bloc_size ";# if $matrix_size / $bloc_size < 101 and $matrix_size % $bloc_size == 0;
	my $renerate_data_requet = system("./../Matrix/generate_data.pl $matrix_size $bloc_size $processor");# if $matrix_size / $bloc_size < 101 and $matrix_size % $bloc_size == 0;
			}
}}


sub calcul_works {
	my $n = shift;
	my $k = shift;
	return 5*($n**2)+(($k+1)/$k)*($n**3);
}


sub calcul_CP {
	my $n = shift;
	my $k = shift;
	return 4*($n**2) + $n*$k + $k**3 - $k**2; 
}



