package Processor;

use strict;
use warnings;
use EndExecuteEvent;
use EndTransferEvent;


sub new {
	my $class = shift;
	my $self = {};
	$self->{id} = shift;
	$self->{simulator} = shift;
	$self->{events} = [];
	bless $self, $class;
	return $self;
}

sub assigned_task{
	my $self = shift;
	my $task = shift;
	my $event;
	my $predecessors = $task->get_predecessors();	
	my $size = get_size_file_necessary($predecessors);
	if($size == 0 ){
		$event = $self->start_task($task);	
	}else{
		$event = $self->start_transfer($size, $task);
	}
	return $event;
}

sub start_task {
	my $self = shift;
	$self->{current_task} = shift;
	my $time = $self->{simulator}->get_time() + $self->{current_task}->get_time();
	my $new_event = EndExecuteEvent->new($time, $self);
	return $new_event;
}

sub start_transfer{
	my $self = shift;
	my $file_size = shift;
	$self->{current_task} = shift;
	return EndTransferEvent->new($file_size,$self->{current_task});
}

sub finish_current_task {
	my $self = shift;
	my @events;
#	if (defined $self->{current_task}) {
		@events = $self->{simulator}->task_finished($self);
		$self->{current_task} = undef;
		#	}
	return @events;
}

sub get_id{
	my $self = shift;
	return $self->{id};
}

sub get_current_task{
	my $self = shift;
	return $self->{current_task};
}

sub get_size_file_necessary{
	my $self = shift;
	my $predecessors = shift;
	return 0;
}
1;
