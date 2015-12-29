#!/usr/bin/env perl

use strict;
use warnings;

die "please give processors number " unless $ARGV[0]=~/^\d+$/;

my $processors_number = $ARGV[0];

my $name = "M_recursivity_file";
my @matrix_size_values = (1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000);
my @recursivity_levels = (1, 2, 3, 4);

for my $matrix_size (@matrix_size_values){
	for my $recursivity_level (@recursivity_levels){
		print $matrix_size." ".$recursivity_level." ";
		my $renerate_data_requet = system("./../Matrix/generate_data_recursive.pl $matrix_size $recursivity_level > multiply_by_recursivity/".$name."".$matrix_size."_".$recursivity_level.".data");
		my $schedul_requet = system("./../schedule.pl multiply_by_recursivity/".$name."".$matrix_size."_".$recursivity_level.".data $processors_number");

		my $expected_time = system("./../expected_time.pl multiply_by_recursivity/".$name."".$matrix_size."_".$recursivity_level.".data $processors_number");

	}
}
