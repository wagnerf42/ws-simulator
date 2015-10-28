package EndExecuteEvent;

use strict;
use warnings;
use Event;

use parent 'Event';

sub new {
	my $class = shift;
	my $self = {};
	$self->{time} = shift;
	$self->{processor} = shift;
	$self->{task} = $self->{processor}->{current_task};
	bless $self, $class;
	return $self;
}

sub display {
		my $self = shift;
		print "processor P".$self->{processor}->{id}." will finished task ".$self->{task}->{name}." at $self->{time}\n";
				return;
			}

sub execute {
	my $self = shift;
	return $self->{processor}->finish_current_task();
}

1;
