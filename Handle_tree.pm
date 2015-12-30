package Handle_tree;

use strict;
use warnings;
use Task;
use Path;

sub new {
	my $class = shift;
	my $self = {};
	my $tasks_file = shift;
	bless $self, $class;
	$self->{tasks} = load_tasks($tasks_file);
	$self->{successors_task} = get_successors($self->{tasks});
	$self->{init_tasks} = [];
	return $self;
	
}

sub handle_tree {
	my $self = shift;
	$self->{paths} = $self->treat_tree($self->{tasks});	
	return;
}

sub get_critical_path {
	my $self = shift;
	my @sorted_paths = sort {$a->get_time() <=> $b->get_time()} @{$self->{paths}};
	my $path = pop @sorted_paths;
	return $path->get_time();
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

sub treat_tree {
	my $self = shift;
	$self->{works} = 0;
	my @paths;
	for my $task_name (keys(%{$self->{tasks}})){
		$self->{works} += $self->{tasks}->{$task_name}->get_time(); 
		my @path = $self->get_paths($task_name) if $self->{tasks}->{$task_name}->is_ready();;
		push @paths, @path;
	}
	return \@paths;
}	

sub get_paths {
	my $self = shift;
	my $current_task_name = shift;
	my @new_paths;
	if (exists $self->{successors_task}->{$current_task_name}){
		for my $succ_task_name (@{$self->{successors_task}->{$current_task_name}}){
			my @paths = $self->get_paths($succ_task_name);
			for my $path (@paths){	
				push @new_paths, $path->add_tasks($self->{tasks}->{$current_task_name}); 
			}			
		}
	}else{
		push @new_paths, Path->new([$current_task_name], $self->{tasks}->{$current_task_name}->get_time());
	}
	return @new_paths;
}

sub get_works {
	my $self = shift;
	return $self->{works};
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

1;
