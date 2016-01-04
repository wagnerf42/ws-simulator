package Handle_tree;

use strict;
use warnings;

my $results_file = $ARGV[0];
die "please give following args : $results_file" unless -f $results_file ;


trait_file($results_file);

sub trait_file{
    my $filename = shift;
	open(FILE, '<', $filename) or die "cannot open file $filename";
	my $line = <FILE>;
	chomp($line);		
	my @split_line = split(/ /,$line);	
	print $split_line[0]." ; ".$split_line[1]." ; ".$split_line[2]." ; ".$split_line[3]." ; W/D ; D-W ; ";	
	print $split_line[4]."; ".$split_line[5]." ; T_attendu / T_simul ; T_simul - T_attendu \n";	
	while($line = <FILE>) {
	chomp($line);		        
	@split_line = split(/ /,$line);
	print $split_line[0]." ; ".$split_line[1]." ; ".$split_line[2].";".$split_line[3];
	print "; ". ($split_line[2]/$split_line[3]) ." ; ". ($split_line[3]-$split_line[2]) ." ; "  ;
	print $split_line[4]." ; ".$split_line[5];
	print " ; ". ($split_line[4]/$split_line[5]) ." ; ". ($split_line[5]-$split_line[4] )." \n"  ;
	}
	return;
}
