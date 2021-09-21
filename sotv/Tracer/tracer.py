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

    def __init__(self, local_vars, global_vars, dump):
        self.global_offsets = global_vars
        self.function_offsets = local_vars
        dump.dump = dump.dump[1:]
        self.execution_dump = dump
        self.tracing_graph = {}

        # A dictionary listing how many different values a variable already had
        self.already_used = {}

    def start_trace(self, trace_no_symbols=True):
        """
        Creates the variable trace over the instructions and registers
        """

        # Loop trough dump lines
        for dump_line in self.execution_dump.dump:
            temp_ins = dump_line.executed_instruction

            # Check whether the instruction is relevant by checking if is a load type or a store type
            if temp_ins.opcode in store_opcodes or temp_ins.opcode in load_opcodes:

                # Ignore ra and s0 (fp) registers
                if temp_ins.r1 == "ra" or temp_ins.r1 == "s0":
                    continue

                # Computes the absolute load address
                if temp_ins.r2 == "s0":
                    address = temp_ins.immediate + dump_line.registers["fp"]
                else:
                    address = temp_ins.immediate + dump_line.registers[temp_ins.r2]

                # Computes the offset of the memory operation from fp
                fp_offset = address - dump_line.registers["fp"]
                name_found = False

                # Check for occurrences for local variables
                if temp_ins.function_name in self.function_offsets.keys():
                    for variable_name in self.function_offsets[temp_ins.function_name].keys():
                        if fp_offset == self.function_offsets[temp_ins.function_name][variable_name]:
                            name_found = True
                            self.trace_variable(variable_name, temp_ins, dump_line)

                # Check for occurrences for global variables
                for variable_name in self.global_offsets.keys():
                    if address == self.global_offsets[variable_name]:
                        name_found = True
                        self.trace_variable(variable_name, temp_ins, dump_line)

                # Default name is hex(address) in case of missing symbol, do not trace in case trace_no_symbols == False
                if not name_found and trace_no_symbols:
                    self.trace_variable(hex(address), temp_ins, dump_line)

    def trace_variable(self, variable, temp_ins, dump_line):
        """
        Traces a variable starting from a certain memory operation
        @param variable: The variable name
        @param temp_ins: The instruction from witch the trace starts
        @param dump_line: The dump_line referencing that instruction
        """

        # Check if this variable has been already traced
        if variable not in self.already_used.keys():
            # Initializes the variable different values counter
            self.already_used[variable] = -1

        self.already_used[variable] += 1
        self.add_variable(variable+"_"+str(self.already_used[variable]), temp_ins.r1, dump_line)

        # Check whether is a load type or a store type and starts the trace
        if temp_ins.opcode in load_opcodes:
            self.check_after(temp_ins.modified_register(), variable+"_"+str(self.already_used[variable]), dump_line)
        elif temp_ins.opcode in store_opcodes:
            self.check_before(temp_ins.r1, variable+"_"+str(self.already_used[variable]), dump_line)
            self.check_after(temp_ins.r1, variable+"_"+str(self.already_used[variable]), dump_line)

    def check_before(self, register, variable, dump_line):
        """
        Checks backwards
        @param register: The register involved
        @param variable: The variable name
        @param dump_line: The dump line reference
        """
        # Checks if the trace has gotten to the dump limit
        if self.execution_dump.dump.index(dump_line)-1 < 0:
            return

        # Gets the previous dump line
        line = self.execution_dump.dump[self.execution_dump.dump.index(dump_line)-1]

        # Executes the adapter
        line.executed_instruction.ins_adapter.adapt(register, variable, line, self, False)

    def check_after(self, register, variable, dump_line):
        """
        Checks afterwards
        @param register: The register involved
        @param variable: The variable name
        @param dump_line: The dump line reference
        """
        # Checks if the trace has gotten to the dump limit
        if self.execution_dump.dump.index(dump_line)+1 >= len(self.execution_dump.dump):
            return

        # Gets the next dump line
        line = self.execution_dump.dump[self.execution_dump.dump.index(dump_line)+1]

        # Executes the adapter
        line.executed_instruction.ins_adapter.adapt(register, variable, line, self, True)

    def add_variable(self, variable, register, dump_line):
        """
        Adds a variable to a certain dump_line
        @param variable: The variable name
        @param register: The associated register
        @param dump_line: The dump_line reference
        """
        if dump_line not in self.tracing_graph.keys():
            self.tracing_graph[dump_line] = {}
        if register not in self.tracing_graph[dump_line].keys():
            self.tracing_graph[dump_line][register] = set()
        self.tracing_graph[dump_line][register].add(variable)

    def verify(self):
        """
        Verifies whether the tracer is coherent with the actual register values
        """

        # Dictionaries used to store the variables values
        values = {}
        for dump_line in self.execution_dump.dump:
            if dump_line in self.tracing_graph.keys():
                for register in self.tracing_graph[dump_line].keys():
                    for variable in self.tracing_graph[dump_line][register]:
                        if register == "s0":
                            register = "fp"
                        if variable in values.keys():
                            if register == "zero":
                                if values[variable] != 0:
                                    assert False
                            else:
                                if values[variable] != dump_line.registers[register]:
                                    assert False
                        else:
                            if register == "zero":
                                values[variable] = 0
                            else:
                                values[variable] = dump_line.registers[register]

    def print(self):
        """
        Prints the tracing graph in a human readable way
        """
        for dump_line in self.execution_dump.dump:
            try:
                print(dump_line.executed_instruction.function_name.ljust(10, " ") +
                      dump_line.executed_instruction.readable.ljust(30, " ") + "\t" +
                      str(self.tracing_graph[dump_line]))
            except KeyError:
                print(dump_line.executed_instruction.function_name.ljust(10, " ") +
                      dump_line.executed_instruction.readable.ljust(30, " "))
