package EndTransferEvent;

use strict;
use warnings;
use Event;

use parent 'Event';

# this event happens when a file finishes being transfered

sub new {
	my $class = shift;
	my $self = {};
	$self->{processor_sender} = shift;
	$self->{processor_receiver} = shift;
	$self->{current_task} = shift;
	$self->{predecessor} = shift;
	$self->{file_size} = shift;
	$self->{time} = shift;
	bless $self, $class;
	return $self;
}

sub display {
	my $self = shift;
	print "Processor P".($self->{processor_sender}+1)." finished send file of task ".$self->{predecessor}->{name}."(".$self->{file_size}.") to Processor P".($self->{processor_receiver}->{id}+1)." at ".$self->{time}."\n";
	return;
}

sub execute {
	my $self = shift;
	return $self->{processor_receiver}->finish_transfer($self->{predecessor}, $self->{file_size});
}


1;
