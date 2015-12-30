#!/usr/bin/env perl

use strict;
use warnings;
use Handle_tree;
use Path;
use Task;

my $tasks_file = $ARGV[0];
my $processors_number = $ARGV[1];
die "please give following args : tasks_file number Processoes" unless -f $tasks_file and $processors_number=~/^\d+$/;

my $handle_tree = Handle_tree->new($tasks_file);

$handle_tree->handle_tree();

#print "Works : ".$handle_tree->get_works()." = Critical Path ".$handle_tree->get_critical_path()."\n";


expected_time($handle_tree->get_works(), $handle_tree->get_critical_path(), $processors_number);

sub expected_time {
	my $works = shift;
	my $critical_path = shift;
	my $processors_number = shift;
	my $expected_time = ($works/$processors_number + $critical_path); 
	print $expected_time."\n";
	return $expected_time;
	
}
