package EventQueue;

use strict;
use warnings;
use EndExecuteEvent;
use EndTransferEvent;
use Event;

sub new {
	my $class = shift;
	my $self = {};
	$self->{events} = [];
	bless $self, $class;
	return $self;
}

sub display {
	my $self = shift;
	print scalar(@{$self->{events}}). " "; 
	return;
}

sub add_event {
	my $self = shift;
	my $event = shift;
	push @{$self->{events}}, $event;
	return;
}

sub get_event {
	my $self = shift;
	my @sorted_events = sort {$a->get_time() <=> $b->get_time()} @{$self->{events}};
	my $event = shift @sorted_events;
	$self->{events} = \@sorted_events;
	return $event;
}

1;
