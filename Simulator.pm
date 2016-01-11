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

sub load {
    my $class = shift;
    my $tasks_file = shift;
    my $processor_numbers = shift;
    my $self = {};
    $self->{time} = 0;
    $self->{idle_processors} = [];
    $self->{processor_numbers} = $processor_numbers;
    $self->{tasks} = load_tasks($tasks_file);
    $self->{successors_task} = get_successors($self->{tasks});
    $self->{remaining_tasks} = scalar(values %{$self->{tasks}});
    $self->{ready_tasks} = [];
    $self->{events} = EventQueue->new();
    $self->{tasks_file} = $tasks_file;
    bless $self, $class;
    $self->set_trace_file_header();
    $self->create_processors($processor_numbers);
    $self->create_init_event();
    return $self;
}

sub new {
    my $class = shift;
    my $tasks = shift;
    my $processor_numbers = shift;
    my $tasks_file = shift;
    my $self = {};
    $self->{time} = 0;
    $self->{idle_processors} = [];
    $self->{processor_numbers} = $processor_numbers;
    $self->{tasks} = get_tasks($tasks);
    $self->{successors_task} = get_successors($self->{tasks});
    $self->{remaining_tasks} = scalar(values %{$self->{tasks}});
    $self->{ready_tasks} = [];
    $self->{events} = EventQueue->new();
    $self->{tasks_file} = $tasks_file;
    bless $self, $class;
    $self->set_trace_file_header();
    $self->create_processors($processor_numbers);
    $self->create_init_event();
    return $self;
}


sub create_init_event {
    my $self = shift;
    $self->{ready_tasks} = [grep {$_->is_ready()} values %{$self->{tasks}}];
    
    my $events = $self->assign_tasks_to_idle_processors();
    for my $event (@$events) {
	$self->{events}->add_event($event);
    }
    return;
}

sub assign_tasks_to_idle_processors {
    my $self = shift;
    my @events;
    while($self->has_ready_tasks() and $self->has_idle_processors()) {
    	my $task = shift @{$self->{ready_tasks}};
 	my $processor = shift @{$self->{idle_processors}};
        $processor->{current_task} = $task;
        my $event = $processor->assign_task($task);
   		push @events, $event;
    }
    return \@events;
}

sub run { 
    my $self = shift;
    while ($self->{remaining_tasks} > 0) {
        my $event = $self->{events}->get_event();
	$self->{time} = $event->get_time();
        my @new_events = $event->execute(); 
		for my $event (@new_events){
			$self->{events}->add_event($event);
        }
    }
    $self->add_finish_lines_to_trace();
    $self->create_trace_file(); 
    return $self->{time};
}

sub add_finish_lines_to_trace {
	my $self = shift;
	my $trace_line = "8 ".$self->{time}." Pile PL\n";
	for my $proc (@{$self->{idle_processors}}){
		$trace_line .= "8 ".$self->{time}." P".$proc->get_id()." Pr\n";	
	}
	$trace_line .= "8 ".$self->{time}." TTP P\n";  
	$self->add_trace_line($trace_line);
	return;	
}

sub task_finished {
    my $self = shift;
    my $processor = shift;
    my $id_processor = $processor->get_id();
    my $executed_task = $processor->get_current_task();
    $executed_task->set_execution_processor($processor);
    $self->{remaining_tasks}--;
    $self->update_ready_tasks($executed_task->get_name());
	$processor->{available_files}->{$executed_task->get_name} = $executed_task->get_name;
	unshift @{$self->{idle_processors}}, $processor;
	my $trace_line = "10 ".$self->get_time()." PS P".$id_processor." Idle \"\" \n";
	$self->add_trace_line($trace_line);
    return $self->assign_tasks_to_idle_processors();
}

sub update_ready_tasks {
    my $self = shift;
    my $executed_task_name = shift;
    my $trace_line = "17 ".$self->get_time()." Pile T 1.00 \n";
    for my $successor (@{$self->{successors_task}->{$executed_task_name}}) {
        $self->{tasks}->{$successor}->{remaining_predecessors}--;
        push @{$self->{ready_tasks}}, $self->{tasks}->{$successor} if $self->{tasks}->{$successor}->is_ready() ;
    	$trace_line .= "16 ".$self->get_time()." Pile T 1.00 \n" if $self->{tasks}->{$successor}->is_ready() ; 
	}

    $self->add_trace_line($trace_line);
    return;
}

sub create_processors {
    my $self = shift;
    my $processors_number = shift;
    $self->{idle_processors} = [map {Processor->new($_, $self)} (0..$processors_number-1)];
    return;
}

sub load_tasks{
    my $filename = shift;
    my %tasks;
    open(FILE, '<', $filename) or die "cannot open file $filename";
	while(my $line = <FILE>) {
	chomp($line);
        my @split_line = split(/ /,$line);
        my $task = Task->new($split_line[0], $split_line[1], $split_line[2]);
        my @predecessors;
        @predecessors = @split_line[3..$#split_line]; 
	$task->init_predecessors(\@predecessors);
        $tasks{$task->get_name()} = $task;
    }
	
	return \%tasks;
}

sub has_ready_tasks {
    my $self = shift;
    return scalar(@{$self->{ready_tasks}});
}

sub has_idle_processors {
    my $self = shift;
	return scalar(@{$self->{idle_processors}});
}

sub get_time {
    my $self = shift;
    return $self->{time};
}

sub display_tasks {
    my $self = shift;
    for my $task (@{$self->{tasks}}){
        $task->display();
    }
    return;
}

sub get_task_by_name {
    my $self = shift;
    my $task_name = shift;
    return $self->{tasks}->{$task_name};
}

sub create_trace_file {
	my $self = shift;
	my @file = split("/", $self->{tasks_file});
	my @name = split(/\./, $file[1]);
	my $filename = "../Trace/$name[0]_".$self->{processor_numbers}."_Processors.trace";
	open(FILE, '>', $filename) or die "cannot open file $filename";
	print FILE $self->{trace};
	close(FILE);
}

sub set_trace_file_header {
	my $self = shift;
	my $header_file_name = "./../Trace/header/header_trace_file.trace";    
	open(H_FILE, '<', $header_file_name) or die "cannot open file $header_file_name";
    while(my $line = <H_FILE>) {
		$self->add_trace_line($line);	
	}
	return ;
}

sub add_trace_line {
	my $self = shift;
	my $trace_line = shift;
	$self->{trace} .= $trace_line; 
}

sub get_successors {
	my $tasks = shift;
	my %successors_task;
	for my $task (keys(%$tasks)){
		my $predecessors_tasks = $tasks->{$task}->get_predecessors();
		for my $p (@$predecessors_tasks){
				push @{$successors_task{$p}}, $task;
			}
		}	
	return \%successors_task;
}

sub get_tasks{
    my $tasks = shift;
    my %tasks;
	for my $line (@{$tasks}) {
        my @split_line = split(/ /,$line);
        my $task = Task->new($split_line[0], $split_line[1], $split_line[2]);
        my @predecessors;
        @predecessors = @split_line[3..$#split_line]; 
		$task->init_predecessors(\@predecessors);
        $tasks{$task->get_name()} = $task;
    }
	
	return \%tasks;
}
1;
