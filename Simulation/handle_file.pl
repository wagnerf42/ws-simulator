#!/usr/bin/env perl

use strict;
use warnings;

my $results_file = $ARGV[0];
my $processors_number = $ARGV[1];
die "please give following args : results_file processors number" unless -f $results_file and $processors_number=~/^\d+$/;


trait_file($results_file);

sub trait_file{
    my $filename = shift;
	open(FILE, '<', $filename) or die "cannot open file $filename";
	my $line = <FILE>;
	chomp($line);		
	my @split_line = split(/ /,$line);	
	print $split_line[0]." ; ".$split_line[1]." ; n*(1/p)^(1/3) ; ".$split_line[2]." ; ".$split_line[3]." ; W/D ; D-W ; ";	
	print $split_line[4]."; ".$split_line[5]." ; T_Sequentiel ; T_simul - T_attendu  ; T_Simul - T_Sequentiel \n";	
	while($line = <FILE>) {
	chomp($line);		        
	@split_line = split(/ /,$line);
	my $limit_bloc = $split_line[0]*((1/$processors_number)**(1/3));
	my $t_sequentiel = ($split_line[0]**3)/$processors_number ;
	print $split_line[0]." ; ".$split_line[1]." ; $limit_bloc ; ".$split_line[2].";".$split_line[3];
	print "; ". ($split_line[2]/$split_line[3]) ." ; ". ($split_line[3]-$split_line[2]) ." ; "  ;
	print $split_line[4]." ; ".$split_line[5] ." ; ".$t_sequentiel ;
	print " ; ". ($split_line[5] - $split_line[4]) ." ; ". ($split_line[5] - $t_sequentiel)." \n"  ;
	}
	return;
}
