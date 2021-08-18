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
        instruction = reference.next_instruction

        tracer.add_variable(variable, register, reference)
        tracer.add_variable(variable, instruction.r1, reference)
        tracer.check_after(instruction.modified_register(), variable, instruction)


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        tracer.add_variable(variable, register, reference)


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        instruction = reference.next_instruction
        if instruction.modified_register() != register:
            tracer.add_variable(variable, register, reference)
