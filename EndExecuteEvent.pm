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
		print "processor P".($self->{processor}->{id}+1)." finished a task ".$self->{task}->{name}."(".$self->{task}->{time}.") at $self->{time}\n";
				return;
			}

sub execute {
	my $self = shift;
	my $events = $self->{processor}->finish_current_task();
	return \@{$events};						
}

1;
