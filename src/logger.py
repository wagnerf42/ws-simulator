#!/usr/bin/env python3
"""
module for paje events logging.
provides a Logger class.
"""

class Logger:
    """
    log events for displaying in paje.
    """
    def __init__(self, filename):
        self.file = open(filename, mode="w")
        self.lines = PAJE_HEADER

    def __del__(self):
        self.file.close()

    def add_new_line(self, line):
        """
        update log lines to be saving in the file in the end of execution.
        """
        self.lines += line + "\n"

    def paje_add_cluster(self, time, id_cluster):
        """
        add log to create clusters in the tracer file
        """
        cluster_name = " Cluster" + str(id_cluster)
        line = "6 "+ str(time) \
            + cluster_name  \
            + " C PF " \
            + "\" Cluster " + str(id_cluster) + "\""
        self.add_new_line(line)

    def paje_add_processor(self, time, processor):
        """
        add log to creat processor with its number and its cluster
        """
        processor_name = " P" + str(processor.number)
        cluster_name = " Cluster" + str(processor.cluster)
        line = "6 "+ str(time) + processor_name \
            + " P" + cluster_name \
            + " \" Processor " + str(processor.number) + "\""
        self.add_new_line(line)

    def paje_set_work(self, time, processor, work=0):
        """
        add log to initialise work in a processors.
        """
        processor_name = "P"+ str(processor.number)
        line = "13 " + str(time) +" Work " + processor_name \
            + " " + str(work) +".00"
        self.add_new_line(line)

    def paje_add_work(self, time, processor, work=0):
        """
        add log to add work in a processors.
        """
        processor_name = "P"+ str(processor.number)
        line = "14 " + str(time) +" Work " + processor_name \
            + " " + str(work) +".00"
        self.add_new_line(line)

    def paje_sub_work(self, time, processor, work=0):
        """
        add log to sub work in a processors.
        """
        processor_name = "P"+ str(processor.number)
        line = "15 " + str(time) +" Work " + processor_name \
            + " " + str(work) +".00"
        self.add_new_line(line)


    def paje_update_processor_state(self, time, processor, new_state):
        """
        add log to update processor state in the system.
        """
        processor_name = "P"+ str(processor.number)
        if processor.network_time > processor.current_time:
            self.paje_pop_processor_state(time, processor)
            line = "8 " + str(time) + " PS " + processor_name\
            + " " + new_state
            self.add_new_line(line)
            self.paje_push_processor_state(time, processor, "Sending")
        else:
            line = "8 " + str(time) + " PS " + processor_name\
                + " " + new_state
            self.add_new_line(line)

    def paje_push_processor_state(self, time, processor, new_state):
        """
        add log to Push new processor state saving the existing state
        used when the processor is on state excuting and
        sending tasks.
        """
        processor_name = "P"+ str(processor.number)
        line = "9 " + str(time) + " PS " + processor_name\
            + " " + new_state
        self.add_new_line(line)

    def paje_pop_processor_state(self, time, processor):
        """
        add log to Pop the last state pushed to this processor
        used when the processor finish sending tasks and still execution
        """
        processor_name = "P"+ str(processor.number)
        line = "10 " + str(time) + " PS " + processor_name
        self.add_new_line(line)

    def paje_start_communication(self, time, source, distination, data=""):
        """
        add log to start link between source and distination.
        key comunication define like "key = source-distination"
        """
        source_name = " P"+ str(source.number)
        if source.cluster == distination.cluster:
            line = "11 " + str(time) + source_name + " " \
                + str(source.number) + "-" + str(distination.number) \
                + " \"" + str(data) + "\"" \
                + " Cluster" + str(distination.cluster) + " IReq_Res"
        else:
            line = "11 " + str(time) + str(source_name) + " " \
                + str(source.number) + "-" + str(distination.number) \
                + " \"" + str(data) + "\"" \
                + " Cluster" + str(distination.cluster) + " EReq_Res"

        self.add_new_line(line)

    def paje_end_communication(self, time, source, distination, data=""):
        """
        add log to end link between source and distination.
        key comunication is define like "source-distination"
        """
        distination_name = " P"+ str(distination.number)
        if source.cluster == distination.cluster:
            line = "12 " + str(time) + distination_name + " " \
                + str(source.number) + "-" + str(distination.number)\
                + " \"" + data + "\"" \
                + " Cluster" + str(distination.cluster) + " IReq_Res"
        else:
            line = "12 " + str(time) + str(distination_name) + " " \
                + str(source.number) + "-" + str(distination.number)\
                + " \"" + data + "\"" \
                + " Cluster" + str(distination.cluster) + " EReq_Res"

        self.add_new_line(line)

    def paje_end_of_logger(self, time, clusters_number, processors_number):
        """
        add log to Destroy system information.
        """
        line = "\n"
        for id_processor in range(processors_number):
            line += "7 " + str(time) + " P" + str(id_processor) + " P \n"

        for id_cluster in range(clusters_number):
            line += "7 " + str(time) + " Cluster" + str(id_cluster) \
                + " C \n"

        line += "7 " + str(time) + " PF S \n"
        self.add_new_line(line)
        print(self.lines, file=self.file)



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
2 PS P "Processor State"
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
