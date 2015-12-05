#!/usr/bin/env perl

use strict;
use warnings;
use Matrix;

die 'needed args :  matrix_size  block_size ' unless defined $ARGV[1] and $ARGV[0]=~/^\d+$/ and $ARGV[1]=~/^\d+$/ ;


my $matrix_a = Matrix->new('a',$ARGV[0],$ARGV[0]);
my $matrix_b = Matrix->new('b',$ARGV[0],$ARGV[0]);
my $bloc_size = $ARGV[1];

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
	my $pred_C;
	for my $i (1..($blocs_number)) {
		for my $j (1..($blocs_number)) {
				my $s = 0;
				my $pred = "";
			for my $k (1..($blocs_number)) {
				print $a->get_name().$i.$k.$b->get_name().$k.$j." ".($bloc_size**3)." ". $bloc_size**2 ." ".$a->get_name().$i.$k." ".$b->get_name().$k.$j." \n";
				$pred .= $a->get_name().$i.$k.$b->get_name().$k.$j." ";
			}
			print "C".$i.$j." ".$bloc_size**2 ." ". $bloc_size**2 ." ". $pred."\n";
			$pred_C .="C".$i.$j." "; 		
		}
	}

	print "Fusion ". (2 * ($a->get_size()**2)) ." ". ($a->get_size()**2) ." ".$pred_C ."\n";
	return;
}	
