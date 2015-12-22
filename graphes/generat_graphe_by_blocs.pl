#!/usr/bin/env perl

use strict;
use warnings;


my $name = "file";
#my $matrix_size = 10;
#my $bloc_size = 5;
my @matrix_size_values = (8, 16, 24, 32, 40, 48, 56);
my @bloc_size_values = (2, 4, 8);

for my $matrix_size (@matrix_size_values){
	for my $bloc_size (@bloc_size_values){
		print $matrix_size." ".$bloc_size." ";
		my $renerate_data_requet = system("./../Matrix/generate_data.pl $matrix_size $bloc_size > multiply_by_blocs/".$name."".$matrix_size."_".$bloc_size.".data");
		my $schedul_requet = system("./../schedule.pl multiply_by_blocs/".$name."".$matrix_size."_".$bloc_size.".data 10");
	}
}
