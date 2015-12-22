#!/usr/bin/env perl

use strict;
use warnings;

use Simulator;

my $tasks_file = $ARGV[0];
my $processors = $ARGV[1];

die "please give following args : tasks_file processors_number" unless -f $tasks_file and $processors=~/^\d+$/;

my $simulator = Simulator->new($tasks_file, $processors);

$simulator->run();

print  $simulator->get_time() ."\n";
