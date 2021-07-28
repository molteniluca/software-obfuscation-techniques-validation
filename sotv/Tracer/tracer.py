"""
main class that take a map of offset and instruction
and create a graph that follow the instructions in the registers

node --  a map[at this instruction, map[in this registers, there are this list of important variables]]
offsets -- a map[variables, offset with fp]
instructions -- the instructions of the program
"""
from sotv.EDG import execution_dump


class Tracer:
    tracing_graph: dict  # {str(ref ins), { register, [str(var)]}
    function_offsets: dict  # initialize by file
    global_offsets: dict
    execution_dump: execution_dump.ExecutionDump

    """
    start the tracing of important value in the code by checking lw offset and comparing this to 
    offsets that we received from the dump
    """

    def start_trace(self):
        for ref in self.execution_dump.dump:
            temp_ins = self.execution_dump.instructions.get(ref.ref_next_instruction)
            if temp_ins.opcode.str == 'lw':
                for ofs in self.function_offsets:
                    if ofs in self.function_offsets:
                        self.tracing_graph[ref.ref_next_instruction] = {temp_ins.modified_register, ofs.variables}
                        self.check_after(temp_ins.modified_register, temp_ins)

    def get_variable(self, instruction):
        pass

    def check_before(self, register, instruction):
        pass

    def check_after(self, register, instruction):
        pass
