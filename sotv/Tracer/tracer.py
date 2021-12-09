"""
main class that take a map of offset and instruction
and create a graph that follow the instructions in the registers

node --  a map[at this instruction, map[in this registers, there are this list of important variables]]
offsets -- a map[variables, offset with fp]
instructions -- the instructions of the program
"""
from typing import Dict

from sotv.EDG import execution_dump
from sotv.EDG.execution_dump import DumpLine
from sotv.Tracer.defines import store_opcodes, load_opcodes
from sotv.Tracer.structures import Register, ignored_registers


class Tracer:
    tracing_graph: Dict[DumpLine, Dict[Register, Dict[str, Dict[str, bool]]]]
    function_offsets: Dict[str, Dict[str, int]]  # initialize by file
    global_offsets: Dict[str, int]
    execution_dump: execution_dump.ExecutionDump

    def __init__(self, local_vars, global_vars, dump, tmp_variables_propagation=10):
        self.tmp_variables_propagation = tmp_variables_propagation
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
        print("Dump length:" + str(len(self.execution_dump.dump)))
        i = 0
        old_percentage = 0
        # Loop trough dump lines
        for dump_line in range(len(self.execution_dump.dump)):
            if old_percentage < int(i/len(self.execution_dump.dump)*100):
                old_percentage = int(i/len(self.execution_dump.dump)*100)
                print("Progress: " + str(int(i/len(self.execution_dump.dump)*100)) + "%")
            i += 1

            temp_ins = self.execution_dump.dump[dump_line].executed_instruction

            # Check whether the instruction is relevant by checking if is a load type or a store type
            if temp_ins.opcode in store_opcodes or temp_ins.opcode in load_opcodes:

                # Ignore ra and s0 (fp) registers
                if temp_ins.r1 in ignored_registers:
                    continue

                variable_name, address = self.find_variable_name(temp_ins, dump_line)

                if variable_name is not None:
                    self.trace_variable(variable_name, temp_ins, dump_line)
                elif trace_no_symbols:
                    self.trace_variable(hex(address), temp_ins, dump_line)

        new_graph = {}
        for el in self.tracing_graph.keys():
            new_graph[self.execution_dump.dump[el]] = self.tracing_graph[el]

        self.tracing_graph = new_graph

    def find_variable_name(self, temp_ins, dump_line):
        # Computes the absolute load address
        if temp_ins.r2 == "s0":
            address = temp_ins.immediate + 0xa0000000
        else:
            address = temp_ins.immediate + 0xb0000000

        # Computes the offset of the memory operation from fp
        fp_offset = address - 0xa0000000

        # Check for occurrences for local variables
        if temp_ins.function_name in self.function_offsets.keys():
            for variable_name in self.function_offsets[temp_ins.function_name].keys():
                if fp_offset == self.function_offsets[temp_ins.function_name][variable_name]:
                    return variable_name, address

        # Check for occurrences for global variables
        for variable_name in self.global_offsets.keys():
            if address-0xb0000000 == self.global_offsets[variable_name]:
                return variable_name, address
        # Default name is hex(address) in case of missing symbol, do not trace in case trace_no_symbols == False
        return None, address

    def trace_variable(self, variable, temp_ins, dump_line):
        """
        Traces a variable starting from a certain memory operation
        @param variable: The variable name
        @param temp_ins: The instruction from witch the trace starts
        @param dump_line: The dump_line referencing that instruction
        """
        if temp_ins.r1 == "zero":
            return

        # Check if this variable has been already traced
        if variable not in self.already_used.keys():
            # Initializes the variable different values counter
            self.already_used[variable] = -1

        self.already_used[variable] += 1
        self.add_variable((variable, dump_line, False), temp_ins.r1, dump_line)

        # Check whether is a load type or a store type and starts the trace
        if temp_ins.opcode in load_opcodes:
            self.check_after(temp_ins.modified_register(), (variable, dump_line, False), dump_line)
        elif temp_ins.opcode in store_opcodes:
            self.check_before(temp_ins.r1, (variable, dump_line, False), dump_line)
            self.check_after(temp_ins.r1, (variable, dump_line, False), dump_line)

    def check_before(self, register, variable, dump_line):
        """
        Checks backwards
        @param register: The register involved
        @param variable: The variable name
        @param dump_line: The dump line reference
        """

        continue_tracing = True
        i = 1
        while continue_tracing:
            # Checks if the trace has gotten to the dump limit
            if dump_line-i < 0:
                return
            if variable[2]:
                if variable[3] == 0:
                    return
                else:
                    variable = (variable[0], variable[1], variable[2], variable[3]-1)
            # Gets the previous dump line
            line = dump_line-i

            # Executes the adapter
            continue_tracing = self.execution_dump.dump[line].executed_instruction.ins_adapter.adapt(register, variable, line, self, False)
            i += 1

    def check_after(self, register, variable, dump_line):
        """
        Checks afterwards
        @param register: The register involved
        @param variable: The variable name
        @param dump_line: The dump line reference
        """
        continue_tracing = True
        i = 1
        while continue_tracing:
            # Checks if the trace has gotten to the dump limit
            if dump_line+i >= len(self.execution_dump.dump):
                return

            if variable[2]:
                if variable[3] == 0:
                    return
                else:
                    variable = (variable[0], variable[1], variable[2], variable[3] - 1)
            # Gets the next dump line
            line = dump_line+i

            # Executes the adapter
            continue_tracing = self.execution_dump.dump[line].executed_instruction.ins_adapter.adapt(register, variable, line, self, True)
            i += 1

    def add_variable(self, variable: (str, int, bool), register, dump_line):
        """
        Adds a variable to a certain dump_line
        @param variable: The variable name
        @param register: The associated register
        @param dump_line: The dump_line reference
        """
        if dump_line not in self.tracing_graph.keys():
            self.tracing_graph[dump_line] = {}
        if register not in self.tracing_graph[dump_line].keys():
            self.tracing_graph[dump_line][register] = dict()

        if len(variable) == 3:
            name, num, tmp = variable
        else:
            name, num, tmp, count = variable

        if name not in self.tracing_graph[dump_line][register].keys():
            self.tracing_graph[dump_line][register][name] = {}

        if num in self.tracing_graph[dump_line][register][name].keys():
            self.tracing_graph[dump_line][register][name][num] = self.tracing_graph[dump_line][register][name][num] and tmp
        else:
            self.tracing_graph[dump_line][register][name][num] = tmp

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
