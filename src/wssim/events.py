"""
module des evenemenet
"""
import wssim
# pylint: disable=too-few-public-methods


class Event():
    """
    Base event class for all events in the system.
    do not use directly but derive from.
    """

    def __init__(self, time, processor, event_type):
        self.time = time
        self.processor = processor
        self.event_type = event_type

    def execute(self):
        """
        log some information on event executions.
        """
        if __debug__:
            if wssim.LOGGING:
                print(self)

    def __str__(self):
        if self.processor is not None:
            return "t={} p={} type:{}".format(self.time,
                                              self.processor.number,
                                              self.event_type)
        else:
            return "t={} type:{}".format(self.time, self.event_type)

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        # only one event for each processor
        return id(self) == id(other)


class IdleEvent(Event):
    """
    Class of Idle_event
    """

    def __init__(self, becomming_idle_time, processor):
        super().__init__(becomming_idle_time, processor, "IDLE")

    def execute(self):
        """
        execute Idle Event
        """
        super().execute()
        self.processor.idle_event()

    def display(self):
        """
        display event
        """
        print("P", self.processor.number, "becomming idle at ", self.time)


class StealRequestEvent(Event):
    """
    a steal request event happens when a victim receives a steal request.
    """

    def __init__(self, steal_time, stealer, victim):
        super().__init__(steal_time, stealer, "REQUEST")
        self.victim = victim

    def execute(self):
        """
        execute steal_request_event
        """
        super().execute()
        self.victim.answer_steal_request(self.processor)

    def display(self):
        """
        display event
        """
        print("P", self.victim.number, " receive work request from P",
              self.processor.number, " at ", self.time)


class StealAnswerEvent(Event):
    """
    a steal answer event happens when a stealer receives answer from
    his victim. it contains the stolen work amount or 0 in case of
    failure.
    """

    def __init__(self, reply_time, stealer, victim, stolen_task):
        super().__init__(reply_time, stealer, "ANSWER")
        self.victim = victim
        self.stolen_task = stolen_task

    def execute(self):
        """
        execute Steal Answer
        """
        super().execute()
        # self.victim.frees_network()
        self.processor.steal_answer(self.stolen_task, self.victim)

    def display(self):
        """
        display event
        """

        print("P", self.processor.number, " receive response (",
              self.stolen_task, ") from P", self.victim.number,
              " at ", self.time)
