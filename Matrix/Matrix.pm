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

sub recursivity_split {
	my $self = shift;
	print "split-$self->{name} ". 2 * $self->{size} ." ".$self->{size}." \n";
	return $self->generate_recursivity_split_tasks();
}	

sub generate_recursivity_split_tasks {
    my $self = shift;
	my $bloc_size = $self->{lines_number} / 2 ;
	my @blocs;
	for my $i (1..4){
		my $bloc = Matrix->new($self->{name}.$i, $bloc_size, $bloc_size);	
		print "$self->{name}$i 0 ". $bloc_size**2 ." split-$self->{name} \n";
		push @blocs, $bloc;		
		}
	return @blocs;
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

sub get_blocs {
	my $self = shift;
	my $bloc_size = $self->{lines_number} / 2;
	my @blocs;
	for my $i (1..4){
		my $bloc = Matrix->new($self->{name}.$i, $bloc_size, $bloc_size);
		push @blocs, $bloc;
	}
	return @blocs;
}

1;	
