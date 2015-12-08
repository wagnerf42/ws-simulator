package Matrix;

use strict;
use warnings;

sub new {
	my $class = shift;
	my $self = {};
	$self->{name} = shift;
	$self->{lines_number} = shift;
	$self->{columns_number} = shift;
	bless $self, $class;
	$self->{size} = $self->{lines_number} * $self->{lines_number} ;
	return $self;
}

sub split {
	my $self = shift;
	my $bloc_size = shift;
	print "split-$self->{name} ". 2 * $self->{size} ." ".$self->{size}." \n";
	$self->generate_split_tasks($bloc_size);
	return;
}

sub generate_split_tasks {
	my $self = shift;
	my $bloc_size = shift;
	my $blocs_number = $self->{lines_number} / $bloc_size ; 
	for my $i (1..$blocs_number){
		for my $j (1..$blocs_number){
			print "$self->{name}$i$j 0 ". $bloc_size**2 ." split-$self->{name} \n";
		}
	}

}

sub get_size {
	my $self = shift;
	return $self->{lines_number};
}

sub get_name {
	my $self = shift;
	return $self->{name};
}
1;
