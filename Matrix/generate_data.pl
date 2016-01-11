#!/usr/bin/env perl

use strict;
use warnings;
use Matrix;
use Simulator;

die 'needed args :  matrix_size  block_size processors_number' unless defined $ARGV[1] and $ARGV[0]=~/^\d+$/ and $ARGV[1]=~/^\d+$/ and $ARGV[2]=~/^\d+$/ ;

my $bloc_size = adjust_matrix_size($ARGV[0],$ARGV[1]);
my $matrix_lines_size = $ARGV[0];
my $processors_number = $ARGV[2];

my $matrix_a = Matrix->new('a', $matrix_lines_size);
my $matrix_b = Matrix->new('b',$matrix_lines_size);

my @lines = run_multiplication_by_bloc($matrix_a, $matrix_b, $bloc_size); 

#simul matrix 
my $simulator = Simulator->new(\@lines, $processors_number, "a/file$matrix_lines_size-$bloc_size-$processors_number.txt");
$simulator->run();
#display work, critical Path and expected time 
expected_time($matrix_lines_size,$bloc_size, $processors_number);
#display Simulation time
print  $simulator->get_time() ." \n";

	#print scalar(@lines). "\n";


sub run_multiplication_by_bloc {
	my ($matrix_a, $matrix_b, $bloc_size) = @_;
	my @line;
	push @line, $matrix_a->split($bloc_size);
	push @line, $matrix_b->split($bloc_size);
	push @line, multiply($matrix_a, $matrix_b, $bloc_size);	
	return @line;
}

sub multiply {
	my $a = shift;
	my $b = shift;
	my $bloc_size = shift;
	my $blocs_number = $a->get_size() / $bloc_size;
	my @lines;
	my $multiply_time = $bloc_size**3;
	my $multiply_data_size = $bloc_size**2;
	
	my $addition_time = ($bloc_size**2)*($blocs_number - 1);
	my $addition_data_size = $bloc_size**2;
	
	my $fusion_time = 2 * ($a->get_size()**2); 
	my $fusion_data_size = $a->get_size()**2;
	
	my @fusion_predecessors;
	for my $i (1..($blocs_number)) {
		for my $j (1..($blocs_number)) {
				my $s = 0;
				my @addition_predecessors;
			for my $k (1..($blocs_number)) {
				push @lines, "a".$i.$k."*b".$k.$j." $multiply_time $multiply_data_size a$i-$k b$k-$j ";
				#print "a".$i.$k."*b".$k.$j." $multiply_time $multiply_data_size a".$i.$k." b".$k.$j." \n";
				push @addition_predecessors, "a".$i.$k."*b".$k.$j;
			}
			my $addition_pred = join(" ", @addition_predecessors);
			push @lines, "C".$i."-".$j." $addition_time $addition_data_size $addition_pred "; 
			#print "C".$i."-".$j." $addition_time $addition_data_size $addition_pred \n";
			push @fusion_predecessors, "C".$i."-".$j; 		
		}
	}
	my $fusion_pred = join(" ", @fusion_predecessors);
	push @lines, "Fusion $fusion_time $fusion_data_size $fusion_pred ";
	#print "Fusion $fusion_time $fusion_data_size $fusion_pred \n";
	return @lines;
}

sub adjust_matrix_size {
	my $matrix_size = shift;
	my $blocs_size = shift;
	while($matrix_size % $blocs_size != 0 ) {
		$blocs_size ++ ;
	}
	return $blocs_size;
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

sub expected_time {
	my $m_size = shift;
	my $b_size = shift;	
	my $processors_number = shift;
	my $works = calcul_works($m_size, $b_size);
	my $critical_path = calcul_CP($m_size, $b_size);
	my $expected_time = (($works/$processors_number) + $critical_path); 
	print "$works $critical_path $expected_time ";
	return $expected_time;
	
}
