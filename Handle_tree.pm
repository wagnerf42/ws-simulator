package Handle_tree;

use strict;
use warnings;
use List::Util qw(max sum);
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

sub initial_tasks {
	my $self = shift;
	my @remaining_tasks;
	for my $task (values(%{$self->{tasks}})){
		push @remaining_tasks, $task if $task->is_ready();
	}
	return @remaining_tasks;
}

sub compute_min_execution_time {
	my $self = shift;
	my @remaining_tasks = $self->initial_tasks();
    	# topological sort : associate to each task its min execution time	
	my %seen_predecessors; # associate to each task the number of predecessors already seen in the topological sort
	while (@remaining_tasks) {
        my $task = shift @remaining_tasks;
        my $predecessors = $task->get_predecessors();
        my $min_time;
   	if (@{$predecessors}) {
		$min_time = max @{[map {$self->{min_execution_time}->{$_} +$self->{tasks}->{$_}->get_time()} @{$predecessors}]};
        } else {
            $min_time = 0;
        }
        $self->{min_execution_time}->{$task->get_name()} = $min_time;
        
	for my $successor (@{$self->{successors_task}->{$task->get_name()}}) {
	$seen_predecessors{$successor} = 0 unless exists $seen_predecessors{$successor};
	$seen_predecessors{$successor}++;
	if ($seen_predecessors{$successor} == scalar(@{$self->{tasks}->{$successor}->get_predecessors()})) {
	     push @remaining_tasks, $self->{tasks}->{$successor};
            }
        }
    }    
}


sub critical_path {
	my $self = shift;
	$self->compute_min_execution_time();				
	return max @{[map {$self->{min_execution_time}->{$_->get_name()} + $_->get_time()} values(%{$self->{tasks}})]};
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


sub get_works {
	my $self = shift;
	return sum @{[map {$_->get_time()} values(%{$self->{tasks}}) ]};
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
