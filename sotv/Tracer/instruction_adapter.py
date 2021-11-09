""""
This interface handle the tracing after a specific type of instruction
"""
from sotv.Tracer.defines import load_opcodes, store_opcodes


class AdapterInterface:
    pass

    def adapt(self, register: str, variable: str, reference, tracer, is_check_after: bool):
        """
        This function traces a variable trough the dump
        @param register The register involved with the trace
        @param variable The variable name
        @param reference The dump_line currently handling
        @param tracer The tracer object
        @param is_check_after A boolean representing whether the caller is checking before or afterwards
        """
        pass


class MoveAdapter(AdapterInterface):
    pass

    def adapt(self, register: str, variable: str, reference, tracer, is_check_after: bool) -> bool:
        instruction = tracer.execution_dump.dump[reference].executed_instruction
        if instruction.modified_register() == register:
            if is_check_after:
                return False
            else:
                tracer.check_before(instruction.r2, variable, reference)
                tracer.check_after(instruction.r2, variable, reference)

                tracer.add_variable(variable, register, reference)
                tracer.add_variable(variable, instruction.r2, reference)
                return False
        else:
            if is_check_after:
                tracer.add_variable(variable, register, reference)
                if instruction.r2 == register:
                    tracer.add_variable(variable, instruction.modified_register(), reference)
                    tracer.check_after(instruction.modified_register(), variable, reference)
                return True
            else:
                tracer.add_variable(variable, register, reference)
                return True


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register: str, variable: str, reference, tracer, is_check_after: bool):
        tracer.add_variable(variable, register, reference)
        return True


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register: str, variable, reference, tracer, is_check_after: bool):
        instruction = tracer.execution_dump.dump[reference].executed_instruction

        if variable[2] and (instruction.opcode in load_opcodes or instruction.opcode in store_opcodes) \
                and instruction.modified_register() == register:
            return False

        if (instruction.opcode not in load_opcodes and instruction.opcode not in store_opcodes) \
                and (instruction.r2 == register or instruction.r3 == register):

            tracer.add_variable((variable[0], variable[1], True, 250), instruction.modified_register(), reference)
            if is_check_after:
                tracer.check_after(instruction.modified_register(), (variable[0], variable[1], True, 250), reference)

        if not is_check_after and (instruction.opcode not in load_opcodes and instruction.opcode not in store_opcodes):
            if instruction.modified_register() == register:
                if instruction.r2 != "unused":
                    tracer.check_before(instruction.r2, (variable[0], variable[1], True, 250), reference)
                if instruction.r3 != "unused":
                    tracer.check_before(instruction.r3, (variable[0], variable[1], True, 250), reference)

        if instruction.modified_register() != register:
            tracer.add_variable(variable, register, reference)
            return True
        else:
            if not is_check_after:
                tracer.add_variable(variable, register, reference)
            return False
