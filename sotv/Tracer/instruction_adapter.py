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
        if instruction.modified_register() == register:
            if is_check_after:
                return
            else:
                tracer.check_before(register, variable, reference)

                tracer.add_variable(variable, register, reference)
        else:
            if is_check_after:
                tracer.add_variable(variable, register, reference)
                tracer.check_after(register, variable, reference)
                if instruction.r2 == register:
                    tracer.add_variable(variable, instruction.modified_register(), reference)
                    tracer.check_after(instruction.modified_register(), variable, reference)
            else:
                tracer.check_before(register, variable, reference)

                tracer.add_variable(variable, register, reference)


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        if is_check_after:
            tracer.add_variable(variable, register, reference)
            tracer.check_after(register, variable, reference)


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer, is_check_after):
        instruction = reference.executed_instruction
        if instruction.modified_register() != register:
            tracer.add_variable(variable, register, reference)

            if is_check_after:
                tracer.check_after(register, variable, reference)
            else:
                tracer.check_after(register, variable, reference)
                tracer.check_before(register, variable, reference)
        else:
            if not is_check_after:
                tracer.add_variable(variable, register, reference)
