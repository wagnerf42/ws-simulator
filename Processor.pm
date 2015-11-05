package Processor;

use strict;
use warnings;
use EndExecuteEvent;
use EndTransferEvent;

my $transfer_time = 1;

sub new {
    my $class = shift;
    my $self = {};
    $self->{id} = shift;
    $self->{simulator} = shift;
    $self->{events} = [];
    $self->{available_files} = {};
    bless $self, $class;
    return $self;
}

sub assign_task {
    my $self = shift;
    $self->{current_task} = shift;
    return $self->start_task() if $self->is_ready_to_execute();
    return $self->start_transfer(); 
}

sub is_ready_to_execute {
    my $self = shift;
	return not $self->missing_files_for_task($self->{current_task});
}

sub missing_files_for_task {
    my $self = shift;
    my $task = shift;
    my $predecessors = $task->get_predecessors();
    return grep {not exists $self->{available_files}->{$_}} @$predecessors;
}	

sub start_task {
    my $self = shift;
    my $time = $self->{simulator}->get_time() + $self->{current_task}->get_time();
    my $new_event = EndExecuteEvent->new($time, $self);
    return $new_event;
}

sub start_transfer {
    my $self = shift;
	my @missing_files = $self->missing_files_for_task($self->{current_task});
	my $first_file = $missing_files[0];
	my $predecessor_task = $self->{simulator}->get_task_by_name($first_file);
    my $id_processor_sender = $predecessor_task->get_execution_processor();
    my $size_file = $predecessor_task->get_file_size();
    my $time = $self->{simulator}->get_time() + $size_file * $transfer_time;
    return EndTransferEvent->new($id_processor_sender, $self, $self->{current_task}, $predecessor_task, $size_file, $time);
}

sub finish_current_task {
    my $self = shift;
    return $self->{simulator}->task_finished($self);
}

sub finish_transfer {
    my $self = shift;
    my $predecessor = shift;
    my $predecessor_name = $predecessor->get_name();
    $self->{available_files}->{$predecessor_name} = 1;
    return $self->start_task() if $self->is_ready_to_execute();
    return $self->start_transfer();
}

sub get_id{
    my $self = shift;
    return $self->{id};
}

sub get_current_task{
    my $self = shift;
    return $self->{current_task};
}


1;
