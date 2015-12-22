#!/usr/bin/env perl

use strict;
use warnings;


my $name = "file";
#my $matrix_size = 10;
#my $bloc_size = 5;
my @matrix_size_values = (200, 400, 600, 800);
my @recursivity_levels = (1, 2, 3);

for my $matrix_size (@matrix_size_values){
	for my $recursivity_level (@recursivity_levels){
		print $matrix_size." ".$recursivity_level." ";
		my $renerate_data_requet = system("./../Matrix/generate_data_recursive.pl $matrix_size $recursivity_level > multiply_by_recursivity/".$name."".$matrix_size."_".$recursivity_level.".data");
		my $schedul_requet = system("./../schedule.pl multiply_by_recursivity/".$name."".$matrix_size."_".$recursivity_level.".data 6");
	}
}
