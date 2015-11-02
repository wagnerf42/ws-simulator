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
	bless $self, $class;
	return $self;
}

sub assigned_task {
	#mauvais nom de methode: pas clair -> renommer assign_task
	my $self = shift;
	$self->{current_task} = shift;
	my $event;
	my %predecessors_file; #inutile
	$self->upload_init_predecessor_files();

	return $self->start_task() if $self->is_ready_to_execute();
	return $self->start_transfer(); #on ne sais pas d'ou transferer
}

sub upload_init_predecessor_files{
	my $self = shift;
	my %predecessor_files;
	my $predecessor_names = $self->{current_task}->get_predecessors();
	for my $predecessor_name (@$predecessor_names){
		my $predecessor_task = $self->{simulator}->get_task_by_name($predecessor_name);
		if ($predecessor_task->get_execution_processor() == $self->{id}){
			# ca ne marche pas -> tu vas transferer plusieurs fois les memes donnees
			$predecessor_files{$predecessor_name} = $predecessor_task->get_size_file();
		}else{
			$predecessor_files{$predecessor_name} = -1; # pourquoi mettre -1 ? -> ca n'a pas de sens
		}
	}
	$self->{predecessor_files} = \%predecessor_files; #champ secret -> le renvoyer plutot
	#le nom n'est pas clair

	return;
}

sub is_ready_to_execute{
	my $self = shift;
	my $value = 1;
	my $predecessors = $self->{current_task}->get_predecessors();
	for my $predecessor (@$predecessors) {
		$value = 0 if $self->{predecessor_files}->{$predecessor} == -1;
	}
	return $value;
}

sub start_task {
	my $self = shift;
	my $time = $self->{simulator}->get_time() + $self->{current_task}->get_time();
	my $new_event = EndExecuteEvent->new($time, $self);
	return $new_event;
}

sub start_transfer{
	my $self = shift;
	my $predecessor_names = $self->{current_task}->get_predecessors();

	for my $predecessor_name (@{$predecessor_names}){
		if ($self->{predecessor_files}->{$predecessor_name} == -1) {
			# si c'est egal a -1 ???
			my $predecessor_task = $self->{simulator}->get_task_by_name($predecessor_name);
			my $id_processor_sender	= $predecessor_task->get_execution_processor();
			my $size_file = $predecessor_task->get_size_file();
			my $time = $self->{simulator}->get_time() + $size_file * $transfer_time;
			return EndTransferEvent->new($id_processor_sender, $self, $self->{current_task}, $predecessor_task, $size_file, $time );
		}
	}
	return;
}

sub finish_current_task {
	my $self = shift;
	my $events = $self->{simulator}->task_finished($self);
	return \@{$events}; # ?????
}

sub finish_transfer {
	my $self = shift;
	my $predecessor = shift;
	my $predecessor_name = $predecessor->get_name();
	my $size_file_transfered = shift;
	$self->{predecessor_files}->{$predecessor_name} = $size_file_transfered;
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

sub get_size_file_necessary{
	my $self = shift;
	my $predecessors = shift;
	return 0;
}
1;
