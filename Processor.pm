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
    $self->add_processor_line_to_trace();
    return $self;
}

sub add_processor_line_to_trace {
    my $self = shift;
    my $trace_line = "7 0 P".$self->get_id()." Pr TTP \"P ".$self->get_id()."\" \n";
    $trace_line .= "10 0 PS P".$self->get_id()." Idle \"\" \n";
    $self->{simulator}->add_trace_line($trace_line);
    return;
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
    my $trace_line = "10 ".$self->{simulator}->get_time()." PS P".$self->get_id()." Exec \"".$self->{current_task}->get_name()."\" \n";
    $self->{simulator}->add_trace_line($trace_line);
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
    
    #status du processor
    my $trace_line = "10 ".$self->{simulator}->get_time()." PS P".$self->get_id()." Tr \"".$first_file."\" \n";
    my $key_link = $id_processor_sender."_".$self->get_id()."_".$first_file;
    #start link from sender
    $trace_line .= "11 ".$self->{simulator}->get_time()." P".$id_processor_sender." ".$key_link." \"".$size_file."\" TTP C\n";
   #end link to receiver
    $trace_line .= "12 ".$self->{simulator}->get_time()." P".$self->get_id()." ".$key_link." \"".$size_file."\" TTP C\n";
    $self->{simulator}->add_trace_line($trace_line);
	
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
