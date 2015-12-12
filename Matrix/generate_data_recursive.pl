#!/usr/bin/env perl

use strict;
use warnings;
use Matrix;

die 'needed args :  matrix_size and  max_recursion_level ' unless defined $ARGV[1] and $ARGV[0]=~/^\d+$/ and $ARGV[1]=~/^\d+$/ ;


my $matrix_a = Matrix->new('a',$ARGV[0],$ARGV[0]);
my $matrix_b = Matrix->new('b',$ARGV[0],$ARGV[0]);
my $matrix_out = Matrix->new('c',$ARGV[0],$ARGV[0]);

my $recursion_level = $ARGV[1];

run_multiplication_by_recursion($matrix_a, $matrix_b, $matrix_out, $recursion_level); 


sub run_multiplication_by_recursion {
	my ($matrix_a, $matrix_b, $matrix_out, $recursion_level) = @_;
	my $out = $matrix_out->get_name(); 
	if($recursion_level == 0){
		matrix_multiply($matrix_a, $matrix_b, $matrix_out);	
	}else{
		my @blocs_a = $matrix_a->recursivity_split();
		my @blocs_b = $matrix_b->recursivity_split();
		my @blocs_out = $matrix_out->get_blocs();
		generate_subresult($blocs_out[0], $blocs_a[0], $blocs_b[0], $blocs_a[1], $blocs_b[2], $recursion_level-1);
		generate_subresult($blocs_out[1], $blocs_a[0], $blocs_b[1], $blocs_a[1], $blocs_b[3],$recursion_level-1);
		generate_subresult($blocs_out[2], $blocs_a[2], $blocs_b[0], $blocs_a[3], $blocs_b[2],$recursion_level-1);
		generate_subresult($blocs_out[3], $blocs_a[2], $blocs_b[1], $blocs_a[3], $blocs_b[3],$recursion_level-1);
		my $sub = join(' ', map {$blocs_out[$_]->get_name()} (0..3));
		matrix_fuse($matrix_out, \@blocs_out);
	}
	return;
}

sub generate_subresult {
	my ($out, $a1, $b1, $a2, $b2, $recursion_level) = @_;
	my $out_1 = Matrix->new("l".$out->get_name(), $a1->get_size(), $a1->get_size());
	my $out_2 = Matrix->new("r".$out->get_name(), $a2->get_size(), $a2->get_size());
	run_multiplication_by_recursion($a1, $b1, $out_1, $recursion_level);
	run_multiplication_by_recursion($a2, $b2, $out_2, $recursion_level);
	matrix_add($out,$out_1,$out_2);
}

sub matrix_multiply {
	my ($a, $b, $out) = @_ ;	
	print $out->get_name()." ".($out->get_size()**3)." ".($out->get_size()**2)." ".$a->get_name()." ".$b->get_name()." \n";
	return;
}	

sub matrix_fuse {
	my $out = shift;
	my $blocs = shift;
	print $out->get_name()." ";
	print (2 * $out->get_size()**2);
	print " ";
	print ($out->get_size()**2);
	for my $bloc (@$blocs){
		print " ".$bloc->get_name();
	}
	print " \n";
	return;
}

sub matrix_add {
	my ($out, $a, $b) = @_;
	print $out->get_name()." ";
	print (($out->get_size()**2)*4);
	print " ".$out->get_size()**2;
	print " ".$a->get_name()." ".$b->get_name()." \n";
	return;
}
