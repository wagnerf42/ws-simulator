#!/usr/bin/env perl

use strict;
use warnings;


die "please give processors number " unless $ARGV[0]=~/^\d+$/;

my $processors_number = $ARGV[0];

my $name = "M_blocs_file";
my @matrix_size_values = (1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000);
my @bloc_size_values = (100, 200, 300, 400, 500, 600);

for my $matrix_size (@matrix_size_values){
	for my $bloc_size (@bloc_size_values){
		print $matrix_size." ".$bloc_size." ";
		my $renerate_data_requet = system("./../Matrix/generate_data.pl $matrix_size $bloc_size > multiply_by_blocs/".$name."".$matrix_size."_".$bloc_size.".data");
		my $schedul_requet = system("./../schedule.pl multiply_by_blocs/".$name."".$matrix_size."_".$bloc_size.".data $processors_number");
		my $expected_time = system("./../expected_time.pl multiply_by_blocs/".$name."".$matrix_size."_".$bloc_size.".data $processors_number");

	}
}
