#!/usr/bin/env python3.5
"""
module for paje events logging.
provides a Logger class.
"""

class Logger:
    """
    log events for displaying in paje.
    """
    def __init__(self, filename, simulator):
        self.file = open(filename, mode="w")
        self.simulator = simulator
        print(PAJE_HEADER, file=self.file)

    def add_cluster(self, id_cluster):
        """
        add log to create clusters in the tracer file
        """
        print("6 {} Cluster{} C PF \"Cluster {}\"".format(
            *[str(i) for i in (self.simulator.time, id_cluster, id_cluster)]),
              file=self.file)

    def add_processor(self, processor):
        """
        add log to create processor with its number and its cluster
        """
        print("6 {} P{} P Cluster{} \"Processor {}\"".format(
            *[str(i) for i in (self.simulator.time, processor.number,
                               processor.cluster, processor.number)]),
              file=self.file)
        # add initial work

        print("6 {} W{} W P{} \"Work processor\"".format(
            *[str(i) for i in (self.simulator.time,
                               processor.number, processor.number)]),
              file=self.file)

    def set_work(self, processor, work=0):
        """
        add log to initialise work in a processors.
        """
        print("13 {} Work W{} {}.00 ".format(
            *[str(i) for i in(self.simulator.time, processor.number, work)]),
              file=self.file)

    def add_work(self, processor, work=0):
        """
        add log to add work in a processors.
        """
        print("14 {} Work W{} {}.00 ".format(
            *[str(i) for i in(self.simulator.time, processor.number, work)]),
              file=self.file)

    def sub_work(self, processor, work=0):
        """
        add log to sub work in a processors.
        """
        print("15 {} Work W{} {}.00 ".format(
            *[str(i) for i in(self.simulator.time, processor.number, work)]),
              file=self.file)

    def update_processor_state(self, processor, new_state):
        """
        add log to update processor state in the system.
        """
        if processor.network_time > processor.current_time:
            self.pop_processor_state(processor)

            print("8 {} PS P{} {}".format(
                *[str(i) for i in (self.simulator.time,
                                   processor.number, new_state)]),
                  file=self.file)

            self.push_processor_state(processor, "Sending")
        else:
            print("8 {} PS P{} {}".format(
                *[str(i) for i in (self.simulator.time,
                                   processor.number, new_state)]),
                  file=self.file)

    def push_processor_state(self, processor, new_state):
        """
        add log to Push new processor state saving the existing state
        used when the processor is on state excuting and
        sending tasks.
        """
        print("9 {} PS P{} {}".format(
            *[str(i) for i in (self.simulator.time,
                               processor.number, new_state)]),
              file=self.file)

    def pop_processor_state(self, processor):
        """
        add log to Pop the last state pushed to this processor
        used when the processor finish sending tasks and still execution
        """
        print("10 {} PS P{} ".format(self.simulator.time, processor.number),
              file=self.file)

    def start_communication(self, source, distination, data=""):
        """
        add log to start link between source and distination.
        key comunication define like "key = source-distination"
        """
        if source.cluster == distination.cluster:
            print("11 {} P{} {}-{} \"{}\" Cluster{} IReq_Res".format(
                *[str(i) for i in (self.simulator.time, source.number,
                                   source.number, distination.number,
                                   data, distination.cluster)]),
                  file=self.file)

        else:
            print("11 {} P{} {}-{} \"{}\" Cluster{} EReq_Res".format(
                *[str(i) for i in (self.simulator.time, source.number,
                                   source.number, distination.number,
                                   data, distination.cluster)]),
                  file=self.file)

    def end_communication(self, source, distination, data=""):
        """
        add log to end link between source and distination.
        key comunication is define like "source-distination"
        """
        if source.cluster == distination.cluster:
            print("12 {} P{} {}-{} \"{}\" Cluster{} IReq_Res".format(
                *[str(i) for i in (self.simulator.time, distination.number,
                                   source.number, distination.number, data,
                                   distination.cluster)]),
                  file=self.file)

        else:
            print("12 {} P{} {}-{} \"{}\" Cluster{} EReq_Res ".format(
                *[str(i) for i in (self.simulator.time, distination.number,
                                   source.number, distination.number, data,
                                   distination.cluster)]),
                  file=self.file)

    def end_of_logger(self, clusters_number, processors_number):
        """
        add log to Destroy system information.
        """
        for processor_id in range(processors_number):
            print("7 {} P{} P".format(self.simulator.time, processor_id),
                  file=self.file)

        for cluster_id in range(clusters_number):
            print("7 {} Cluster{} Cluster".format(self.simulator.time,
                                                  cluster_id),
                  file=self.file)

        self.file.close()



PAJE_HEADER = """\
%EventDef PajeDefineContainerType 1
% Alias string
% ContainerType string
% Name string
%EndEventDef
%EventDef PajeDefineStateType 2
% Alias string
% ContainerType string
% Name string
%EndEventDef
%EventDef PajeDefineLinkType 3
% Alias string
% ContainerType string
% SourceContainerType string
% DestContainerType string
% Name string
%EndEventDef
%EventDef PajeDefineEntityValue 4
% Alias string
% EntityType string
% Name string
% Color color
%EndEventDef
%EventDef PajeDefineVariableType 5
% Alias string
% Type string
% Name string
% Color color
%EndEventDef
%EventDef PajeCreateContainer 6
% Time date
% Alias string
% Type string
% Container string
% Name string
%EndEventDef
%EventDef PajeDestroyContainer 7
% Time date
% Name string
% Type string
%EndEventDef
%EventDef PajeSetState 8
% Time date
% Type string
% Container string
% Value string
%EndEventDef
%EventDef PajePushState	9
% Time	date
% EntityType	string
% Container	string
% Value	string
%EndEventDef
%EventDef PajePopState 10
% Time    date
% EntityType string
% Container string
%EndEventDef
%EventDef PajeStartLink 11
% Time date
% SourceContainer string
% Key string
% Value string
% Container string
% Type string
%EndEventDef
%EventDef PajeEndLink 12
% Time date
% DestContainer string
% Key string
% Value string
% Container string
% Type string
%EndEventDef
%EventDef PajeSetVariable 13
% Time date
% Type string
% Container string
% Value double
%EndEventDef
%EventDef PajeAddVariable 14
% Time date
% Type string
% Container string
% Value double
%EndEventDef
%EventDef PajeSubVariable 15
% Time date
% Type string
% Container string
% Value double
%EndEventDef

1 S 0 System
1 C S Cluster
1 P C Processor
1 W P Work

2 PS P "Processor State"
5 Work W "Work Amount" "9 0.1 0.1"

3 IReq_Res C P P "Internal Request-Response"
3 EReq_Res C P P "External Request-Response"

4 Executing PS Executing "8 0.8 0.2"
4 Idle PS Idle "2 1.3 1.0"
4 Stealing PS Stealing "1 0.1 0.1"
4 Receiving PS Receiving "8 0.4 0.2"
4 Sending PS Sending "5 0.5 0.7"

5 Work P "Total Work on Processor" "9 0.1 0.1"

6 0 PF S 0 "Plate-forme"
"""
