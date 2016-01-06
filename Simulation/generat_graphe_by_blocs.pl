#!/usr/bin/env perl

use strict;
use warnings;


die "please give processors number " unless $ARGV[0]=~/^\d+$/;

my $processors_number = $ARGV[0];
my $name = "M_blocs_file";
my @matrix_size_values = (2000, 3000, 4000, 5000);
my @bloc_size_values = ( 500,  250, 100);

print "M_size B_size W D T_attendu T_simul \n";
for my $matrix_size (@matrix_size_values){
	for my $bloc_size (@bloc_size_values){
		
		while($matrix_size % $bloc_size != 0 ) {
			$bloc_size ++ ;
		}
		
		print $matrix_size." ".$bloc_size." ";
my $renerate_data_requet = system("./../Matrix/generate_data.pl $matrix_size $bloc_size > multiply_by_blocs/$name-$matrix_size-$bloc_size.data");

#print " | ".calcul_works($matrix_size, $bloc_size) ." > ". calcul_CP($matrix_size, $bloc_size) ." > ";
		
		my $expected_time = system("./../expected_time.pl multiply_by_blocs/$name-$matrix_size-$bloc_size.data $processors_number");
				
		my $schedul_requet = system("./../schedule.pl multiply_by_blocs/$name-$matrix_size-$bloc_size.data $processors_number");
	}
}


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
			
