package Simulator;

use strict;
use warnings;
use EventQueue;
use Event;
use EndExecuteEvent;
use EndTransferEvent;
use Task;
use Processor;
use Task;

sub new{
	my $class = shift;
	my $tasks_file = shift;
	my $processor = shift;
	my $self = {};
	#bless $self, $class;
	$self->{time} = 0;
	$self->{idle_processors} = [];
	$self->{tasks} = load_tasks($tasks_file);
	$self->{remaining_tasks} = scalar(@{$self->{tasks}});
	$self->{ready_tasks} = [];
	$self->{events} = EventQueue->new();
	bless $self, $class;
	$self->create_processors($processor);
	$self->creat_init_event();
	return $self;
}

sub creat_init_event{
	my $self = shift;
	for my $task (@{$self->{tasks}}){
		push @{$self->{ready_tasks}}, $task if $task->is_ready();
	}

	while($self->has_ready_tasks() and $self->has_idle_processors()){
		my $task = shift @{$self->{ready_tasks}};
		my $processor = shift @{$self->{idle_processors}};
		$processor->{current_task} = $task;
		my $event = $processor->start_task($task);
		$self->{events}->add_event($event);
	}

	return;
}

sub run{
	my $self = shift;
	while ($self->{remaining_tasks} > 0) {
		my $event = $self->{events}->get_event();
		$self->{time} = $event->get_time();
		my $new_event = $event->execute();
		$event->display();
		for my $event (@{$new_event}){
			$self->{events}->add_event($event);
		}
	}
	return $self->{time};
}

sub task_finished {
	my $self = shift;
	my $processor = shift;
	my @new_events;
	my $id_processor = $processor->get_id();
	my $executed_task = $processor->get_current_task();
	$self->update_ready_tasks($executed_task, $id_processor);
	unshift @{$self->{idle_processors}}, $processor;
	$self->{remaining_tasks}--;

	while($self->has_ready_tasks() and $self->has_idle_processors()){
		my $task = shift @{$self->{ready_tasks}};
		my $processor = shift @{$self->{idle_processors}};
		my $event = $processor->assigned_task($task);
		push @new_events, $event;
	}

	return \@new_events;
}

sub update_ready_tasks{
	my $self = shift;
	my $executed_task = shift;
	my $id_processor = shift;
	for (my $i=0 ; $i < scalar(@{$self->{tasks}}) ; $i++){
		@{$self->{tasks}}[$i]->{processor} = $id_processor if $executed_task->get_name() eq @{$self->{tasks}}[$i]->get_name();

		my $value = @{$self->{tasks}}[$i]->update_predecessor($executed_task);
		push @{$self->{ready_tasks}},  @{$self->{tasks}}[$i] if @{$self->{tasks}}[$i]->is_ready() and $value == 1; 	
	}
	return;
}

sub create_processors {
	my $self = shift;
	my $processors_number = shift;
	for my $i (0..($processors_number-1)) {
		my $processor = Processor->new($i, $self);
		push @{$self->{idle_processors}}, $processor;
	}
	return;
}

sub load_tasks{
	my $filename = shift;
	my @tasks;
	open(FILE, '<', $filename) or die "cannot open file $filename";
	while(my $line = <FILE>) {
		my @split_line = split(/ /,$line);
		my $task = Task->new($split_line[0], $split_line[1], $split_line[2]);
		my $predecessors = [];
		for (my $i=3 ; $i<scalar(@split_line)-1 ; $i++){
			push @{$predecessors}, $split_line[$i];	
		}
		$task->init_predecessors($predecessors);
		push @tasks, $task;
	}
	return \@tasks;
}

sub has_ready_tasks{
	my $self = shift;
	return scalar(@{$self->{ready_tasks}});
}

sub has_idle_processors{
	my $self = shift;
	return scalar(@{$self->{idle_processors}});
}

sub get_time{
	my $self = shift;
	return $self->{time};
}

sub display_tasks{
	my $self = shift;
	for my $task (@{$self->{tasks}}){
		$task->display();
	}
}

sub get_task_by_name{
	my $self = shift;
	my $task_name = shift;
	for my $task (@{$self->{tasks}}){
		return $task if $task->get_name() eq $task_name;
	}

}

1;
