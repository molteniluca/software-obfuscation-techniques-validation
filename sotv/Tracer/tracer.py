"""
main class that take a map of offset and instruction
and create a graph that follow the instructions in the registers

node --  a map[at this instruction, map[in this registers, there are this list of important variables]]
offsets -- a map[variables, offset with fp]
instructions -- the instructions of the program
"""
from typing import Dict, Set

from sotv.EDG import execution_dump
from sotv.EDG.execution_dump import DumpLine
from sotv.Tracer.structures import Register


class Tracer:
    tracing_graph: Dict[DumpLine, Dict[Register, Set[str]]]  # {str(ref ins), { register, [str(var)]}
    function_offsets: Dict[str, Dict[str, int]]  # initialize by file
    global_offsets: Dict[str, int]
    execution_dump: execution_dump.ExecutionDump

    """
    start the tracing of important value in the code by checking lw offset and comparing this to 
    offsets that we received from the dump
    """

    def __init__(self, local_vars, global_vars, dump):
        self.global_offsets = global_vars
        self.function_offsets = local_vars
        dump.dump = dump.dump[1:]
        self.execution_dump = dump
        self.tracing_graph = {}

    def start_trace(self):
        for dump_line in self.execution_dump.dump:
            temp_ins = dump_line.executed_instruction
            if temp_ins.opcode == 'lw' or temp_ins.opcode == "sw":
                for variable in self.function_offsets[temp_ins.function_name].keys():
                    if self.function_offsets[temp_ins.function_name][variable] == temp_ins.immediate:
                        self.add_variable(variable, temp_ins.r1, dump_line)
                        if temp_ins.opcode == "lw":
                            self.check_after(temp_ins.modified_register(), variable, temp_ins)
                        else:
                            self.check_before(temp_ins.r1, variable, temp_ins)
                            self.check_after(temp_ins.r1, variable, temp_ins)

    def check_before(self, register, variable, instruction):
        dump_lines = self.execution_dump.dump
        dump_lines.reverse()
        for dump_line in dump_lines:
            temp_ins = dump_line.executed_instruction
            if temp_ins == instruction:
                for reference in self.execution_dump.dump:
                    temp_ins = reference.executed_instruction
                    temp_ins.ins_adapter.adapt(register, variable, reference, self)
                    if temp_ins == temp_ins.modified_register():
                        return

    def check_after(self, register, variable, instruction):
        for dump_line in self.execution_dump.dump:
            temp_ins = dump_line.executed_instruction
            if temp_ins == instruction:
                for reference in self.execution_dump.dump:
                    temp_ins = reference.executed_instruction
                    temp_ins.ins_adapter.adapt(register, variable, reference, self)
                    if temp_ins == temp_ins.modified_register():
                        return

    def add_variable(self, variable, register, dump_line):
        if dump_line not in self.tracing_graph.keys():
            self.tracing_graph[dump_line] = {}
        if register not in self.tracing_graph[dump_line].keys():
            self.tracing_graph[dump_line][register] = set()
        self.tracing_graph[dump_line][register].add(variable)
