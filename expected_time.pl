#!/usr/bin/env perl

use strict;
use warnings;
use List::Util qw(max sum);
use Handle_tree;
use Path;
use Task;

my $tasks_file = $ARGV[0];
my $processors_number = $ARGV[1];
die "please give following args : tasks_file number Processoes" unless -f $tasks_file and $processors_number=~/^\d+$/;

my $tree = Handle_tree->new($tasks_file);

#print "Critical Path ".$tree->critical_path()." works : ".$tree->get_works()."\n";

expected_time($tree, $processors_number);

sub expected_time {
	my $tree = shift;
	my $processors_number = shift;
	my $works = $tree->get_works();
	my $critical_path = $tree->critical_path();
	my $expected_time = (($works/$processors_number) + $critical_path); 
	print "$works $critical_path $expected_time ";
	return $expected_time;
	
}
