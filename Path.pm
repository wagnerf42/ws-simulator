package Path;

use strict;
use warnings;
use Task;

sub new {
	my $class = shift;
	my $task = shift;
	my $self = {};
	$self->{time} = shift;
	$self->{tasks} = [];
	bless $self, $class;
	push @{$self->{tasks}}, @{$task};
	return $self;
}

sub get_time {
	my $self = shift;
	return $self->{time};
}

sub add_tasks {
	my $self = shift;
	my $task = shift;
	my $new_tasks = $self->{tasks};
	unshift @{$new_tasks}, $task->get_name();
	my $new_time = $self->{time} + $task->get_time();
	return Path->new($new_tasks,$new_time);
} 

sub display {
	my $self = shift;

	print "time : $self->{time} => ";
	for my $p (@{$self->{tasks}}){
		print $p." ";
	}
	print "\n";
	return;

}
1;
