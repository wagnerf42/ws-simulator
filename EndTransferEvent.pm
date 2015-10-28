package EndTransferEvent;

use strict;
use warnings;
use Event;

use parent 'Event';

sub new {
	my $class = shift;
	my $self = {};
	$self->{size} = shift;	
	$self->{processor} = shift;
	$self->{task} = shift;
	bless $self, $class;
	$self->{time} = $self->{size};	
	return $self;
}

sub display{
	my $self = shift;
	print "processor P".$self->{processor}->{id}." has all file (".$self->{size}.") for a task ".$self->{task}->{name};
	return;
}


sub execute {
	my $self = shift;
	print "execute EndTransferEvent \n";
	return $self->{processor}->start_task($self->{task});
}

1;
