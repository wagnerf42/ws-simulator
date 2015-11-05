package Task;

use strict;
use warnings;

sub new {
    my $class = shift;
    my $self = {};
    $self->{name} = shift;
    $self->{time} = shift;
    $self->{file_size} = shift;
    $self->{predecessors} = {};
    bless $self, $class;
    return $self;
}

sub display {
    my $self = shift;
    print "Task $self->{name} with execution time = $self->{time} and has " . scalar(@{$self->{predecessors}}) ." predecessors \n";
    print "remaining tasks $self->{remaining_predecessors} ==> @{$self->{predecessors}} \n" if scalar(@{$self->{predecessors}}) > 0 ;

    print "execute processor : $self->{processor}\n" if defined $self->{processor};
    return;
}

sub is_ready {
    my $self = shift;
    return $self->{remaining_predecessors} == 0;
}

sub update_predecessor {
    my $self = shift;
    my $task_finished = shift;
	my $value = 0;
	if (exists $self->{predecessors}->{$task_finished}) {
   		$self->{remaining_predecessors}--;
        return 1;
    } else {
        return 0;
    }
}

sub get_predecessors {
    my $self = shift;
	return [values %{$self->{predecessors}} ];
}

sub init_predecessors {
    my $self = shift;
    my $predecessors = shift;
	for my $predecessor (@$predecessors) {
		$self->{predecessors}->{$predecessor} = $predecessor;
    }
    $self->{remaining_predecessors} = scalar(@$predecessors);
	return;
}

sub get_execution_processor {
    my $self = shift;
    return $self->{processor}->get_id();
}

sub get_file_size {
    my $self = shift;
    return $self->{file_size};
}

sub get_name {
    my $self = shift;
    return $self->{name};
}

sub get_time {
    my $self = shift;
    return $self->{time};
}

sub set_execution_processor {
	my $self = shift;
	my $processor = shift;
	$self->{processor} = $processor;
	return;
}
1;
