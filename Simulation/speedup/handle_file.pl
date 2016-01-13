#!/usr/bin/env perl

use strict;
use warnings;

my $results_file = $ARGV[0];
#my $processors_number = $ARGV[1];
die "please give following args : results_file processors number" unless -f $results_file; #and $processors_number=~/^\d+$/;


trait_file($results_file);


sub trait_file{
    my $filename = shift;
	open(FILE, '<', $filename) or die "cannot open file $filename";
	my $line = <FILE>;
	chomp($line);		
	my @split_line = split(/ /,$line);	
	print $split_line[0]." ".$split_line[1]." ".$split_line[2]." ".$split_line[3]." ".$split_line[4]." W/D ";	
	print $split_line[5]." ".$split_line[6]." T_Sequentiel T_simul/T_attendu speedup=(n^3+2*n^2)/T_Simul eff=speedup/nb_proc \n";	
	while($line = <FILE>) {
	chomp($line);		        
	@split_line = split(/ /,$line);
	my $t_sequentiel = ($split_line[1]**3) + 2*($split_line[1]**2) ;

	print $split_line[0]." ".$split_line[1]." ".$split_line[2]." ".$split_line[3]." ".$split_line[4];
	print " ". ($split_line[3]/$split_line[4]) ." "  ;
	print $split_line[5]." ".$split_line[6] ." ".$t_sequentiel ;
	print " ". ($split_line[6] / $split_line[5]) ." ". ($t_sequentiel / $split_line[6])." ".(($t_sequentiel / $split_line[6])/$split_line[0])." \n" ;
	}
	return;
}
