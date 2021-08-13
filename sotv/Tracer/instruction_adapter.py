""""
this interface handle the tracing after a specific type of instruction
"""


class AdapterInterface:
    pass

    def adapt(self, register, variable, reference, tracer):
        pass


class MoveAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        instruction = tracer.execution_dump.instructions.get(reference.ref_next_instruction)
        tracer.tracing_graph[reference.ref_next_instruction] = {instruction,
                                                                variable}  # this assignment is a place holder because is probably wrong
        tracer.check_after(instruction.modified_register(), variable, instruction)


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        pass


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        pass
