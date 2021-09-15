""""
this interface handle the tracing after a specific type of instruction
"""


class AdapterInterface:
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        pass


class MoveAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        instruction = reference.executed_instruction
        tracer.add_variable(variable, register, reference)
        tracer.add_variable(variable, instruction.r1, reference)
        if is_check_after:
            tracer.check_after(instruction.modified_register(), variable, instruction)
        else:
            tracer.check_after(instruction.r2, variable, instruction)
            tracer.check_before(instruction.r2, variable, instruction)


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        tracer.add_variable(variable, register, reference)


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        instruction = reference.executed_instruction
        if instruction.modified_register() != register:
            tracer.add_variable(variable, register, reference)
