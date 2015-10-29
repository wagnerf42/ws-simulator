package Task;

use strict;
use warnings;

sub new {
	my $class = shift;
	my $self = {};
	$self->{name} = shift;
	$self->{time} = shift;
	$self->{size_file} = shift;
	$self->{predecessors} = [];
	bless $self, $class; 
	return $self;
	}

sub display {
	my $self = shift;
	print "Task $self->{name} with execution time = $self->{time} and has " . scalar(@{$self->{predecessors}}) ." predecessors \n";
	print "remaining tasks $self->{remaining_predecessors} ==> @{$self->{predecessors}} \n" if scalar(@{$self->{predecessors}}) > 0 ; 
	
	print "execute processor : $self->{processor}\n" if defined $self->{processor};
	return;
	}

sub is_ready {
	my $self = shift;
	return 1 if $self->{remaining_predecessors} == 0;
	return;
	}

sub update_predecessor{
	my $self = shift;
	my $task_finished = shift;
	my @new_predecessors;
	my $updated = 0;
	for(my $i = 0 ; $i<scalar(@{$self->{predecessors}}) ; $i++){
		if ($task_finished->{name} eq @{$self->{predecessors}}[$i]){
		 	$self->{remaining_predecessors}--;
			$updated = 1;
		}
	}
	return $updated;
}

sub get_predecessors{
	my $self = shift;
	return \@{$self->{predecessors}};
	}

sub init_predecessors{
	my $self = shift;
	my $predecessors = shift;
	push @{$self->{predecessors}}, @{$predecessors};
	$self->{remaining_predecessors} = scalar(@{$predecessors});
	return;
}

sub get_execution_processor{
	my $self = shift;
	return $self->{processor};
	}

sub get_size_file{
	my $self = shift;
	return $self->{size_file};
}

sub get_name{
	my $self = shift;
	return $self->{name};
}

sub get_time{
	my $self = shift;
	return $self->{time};
}	
1;
