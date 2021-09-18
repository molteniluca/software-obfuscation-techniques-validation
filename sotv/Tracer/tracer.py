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
from sotv.Tracer.structures import Register, store_opcodes, load_opcodes


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

        self.already_used = {}

    def start_trace(self):
        for dump_line in self.execution_dump.dump:
            temp_ins = dump_line.executed_instruction
            if temp_ins.opcode in store_opcodes or temp_ins.opcode in load_opcodes:
                if temp_ins.r2 == "s0":
                    address = temp_ins.immediate + dump_line.registers["fp"]
                else:
                    address = temp_ins.immediate + dump_line.registers[temp_ins.r2]
                sp_offset = address - dump_line.registers["fp"]
                name_found = False

                for variable_name in self.function_offsets[temp_ins.function_name].keys():
                    if sp_offset == self.function_offsets[temp_ins.function_name][variable_name]:
                        name_found = True
                        self.trace_variable(variable_name, temp_ins, dump_line)

                for variable_name in self.global_offsets.keys():
                    if address == self.global_offsets[variable_name]:
                        name_found = True
                        self.trace_variable(variable_name, temp_ins, dump_line)

                if not name_found:
                    self.trace_variable(hex(address), temp_ins, dump_line)

    def trace_variable(self, variable, temp_ins, dump_line):
        if variable not in self.already_used.keys():
            self.already_used[variable] = -1
        self.already_used[variable] += 1
        self.add_variable(variable+"_"+str(self.already_used[variable]), temp_ins.r1, dump_line)
        if temp_ins.opcode in load_opcodes:
            self.check_after(temp_ins.modified_register(), variable+"_"+str(self.already_used[variable]), dump_line)
        elif temp_ins.opcode in store_opcodes:
            self.check_before(temp_ins.r1, variable+"_"+str(self.already_used[variable]), dump_line)
            self.check_after(temp_ins.r1, variable+"_"+str(self.already_used[variable]), dump_line)

    def check_before(self, register, variable, dump_line):
        if self.execution_dump.dump.index(dump_line)-1 < 0:
            return
        line = self.execution_dump.dump[self.execution_dump.dump.index(dump_line)-1]
        line.executed_instruction.ins_adapter.adapt(register, variable, line, self, False)

    def check_after(self, register, variable, dump_line):
        if self.execution_dump.dump.index(dump_line)+1 >= len(self.execution_dump.dump):
            return
        line = self.execution_dump.dump[self.execution_dump.dump.index(dump_line)+1]
        line.executed_instruction.ins_adapter.adapt(register, variable, line, self, True)

    def add_variable(self, variable, register, dump_line):
        if dump_line not in self.tracing_graph.keys():
            self.tracing_graph[dump_line] = {}
        if register not in self.tracing_graph[dump_line].keys():
            self.tracing_graph[dump_line][register] = set()
        self.tracing_graph[dump_line][register].add(variable)

    def verify(self):
        for dump_line in self.execution_dump.dump:
            values = {}
            if dump_line in self.tracing_graph.keys():
                for register in self.tracing_graph[dump_line].keys():
                    for variable in self.tracing_graph[dump_line][register]:
                        if variable in values.keys():
                            if values[variable] != dump_line.registers[register]:
                                assert False
                        else:
                            if register == "zero":
                                values[variable] = 0
