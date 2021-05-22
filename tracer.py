"""
main class that take a map of offset and instruction
and create a graph that follow the instructions in the registers

node --  a map[at this instruction, map[in this registers, there are this list of important variables]]
offsets -- a map[variables, offset with fp]
instructions -- the instructions of the program
"""


class Tracer:
    node = {}
    offsets = {}  # initialize by file
    instruction = []  # initialize by file

    def __init__(self, instruction, register, variables):
        self.node = {instruction, {register, variables}}
    """
    start the tracing of important value in the code by checking lw offset and comparing this to 
    offsets that we received from the dump
    """
    def start_trace(self):
        pass

    def get_variable(self, instruction):
        pass

    def check_before(self, register, instruction):
        pass

    def check_after(self, register, instruction):
        pass
