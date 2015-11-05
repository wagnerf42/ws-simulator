package EndTransferEvent;

use strict;
use warnings;
use Event;

use parent 'Event';

sub new {
	my $class = shift;
	my $self = {};
	$self->{processor_sender} = shift;
	$self->{processor_receiver} = shift;
	$self->{current_task} = shift;
	$self->{predecessor} = shift;
	$self->{size_file} = shift;
	$self->{time} = shift;			
	bless $self, $class;
	return $self;
}

sub display {
	my $self = shift;
	print "Processor P".($self->{processor_sender}+1)." finished send file of task ".$self->{predecessor}->{name}."(".$self->{size_file}.") to Processor P".($self->{processor_receiver}->{id}+1)." at ".$self->{time}."\n";
	return;
}

sub execute {
	my $self = shift;
	my $event = $self->{processor_receiver}->finish_transfer($self->{predecessor},$self->{size_file});
	my @events;
	push @events, $event;	
	return @events;                     
}


1;
