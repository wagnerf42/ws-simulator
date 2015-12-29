#!/usr/bin/env perl

use strict;
use warnings;
use Matrix;

die 'needed args :  matrix_size  block_size ' unless defined $ARGV[1] and $ARGV[0]=~/^\d+$/ and $ARGV[1]=~/^\d+$/ ;

my $matrix_lines_size = adjust_matrix_size($ARGV[0],$ARGV[1]);
my $bloc_size = $ARGV[1];
my $matrix_a = Matrix->new('a', $matrix_lines_size);
my $matrix_b = Matrix->new('b',$matrix_lines_size);

run_multiplication_by_bloc($matrix_a, $matrix_b, $bloc_size); 

sub run_multiplication_by_bloc {
	my ($matrix_a, $matrix_b, $bloc_size) = @_;
	$matrix_a->split($bloc_size);
	$matrix_b->split($bloc_size);
	multiply($matrix_a, $matrix_b, $bloc_size);	
	return;
}

sub multiply {
	my $a = shift;
	my $b = shift;
	my $bloc_size = shift;
	my $blocs_number = $a->get_size() / $bloc_size;
	
	my $multiply_time = $bloc_size**3;
	my $multiply_data_size = $bloc_size**2;
	
	my $addition_time = ($bloc_size**2)*4;
	my $addition_data_size = $bloc_size**2;
	
	my $fusion_time = 2 * ($a->get_size()**2); 
	my $fusion_data_size = $a->get_size()**2;
	
	my @fusion_predecessors;
	for my $i (1..($blocs_number)) {
		for my $j (1..($blocs_number)) {
				my $s = 0;
				my @addition_predecessors;
			for my $k (1..($blocs_number)) {
				print "a".$i.$k."*b".$k.$j." $multiply_time $multiply_data_size a".$i.$k." b".$k.$j." \n";
				push @addition_predecessors, "a".$i.$k."*b".$k.$j;
			}
			my $addition_pred = join(" ", @addition_predecessors);
			print "C".$i."-".$j." $addition_time $addition_data_size $addition_pred \n";
			push @fusion_predecessors, "C".$i."-".$j; 		
		}
	}
	my $fusion_pred = join(" ", @fusion_predecessors);
	print "Fusion $fusion_time $fusion_data_size $fusion_pred \n";
	return;
}

sub adjust_matrix_size {
	my $matrix_size = shift;
	my $blocs_size = shift;
	while($matrix_size % $blocs_size != 0 ) {
		$matrix_size ++ ;
	}
	return $matrix_size;
}
