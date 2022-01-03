from typing import List

from sotv.Tracer.instruction import Instruction


class DumpLine:
    """
    This class represents a step in a dump

    :ivar registers a dictionary containing all the register values
    :ivar SP_offsets a dictionary representing the computed offsets of the variables from sp
    :ivar FP_offsets a dictionary representing the computed offsets of the variables from fp
    :ivar var_values a dictionary representing the variables values
    :ivar next_instruction the instruction to be executed
    :ivar ref_next_instruction the reference to the instruction to be executed
    """
    executed_instruction: Instruction
    ref_executed_instruction: str

    def __init__(self, line):
        self.__dict__ = line


class ExecutionDump:
    """
    This class represents an execution dump

    :ivar dump an array representing the execution flow
    :ivar instructions the instructions contained in this program
    """
    instructions: List[Instruction]
    dump: List[DumpLine]

    def __init__(self, instructions_dict, dump):
        self.dump = []

        for line in dump:
            line_obj = DumpLine(line)
            if line_obj.executed_instruction is not None:
                if "+exclude" not in line_obj.ref_executed_instruction:
                    line_obj.executed_instruction = instructions_dict[line_obj.ref_executed_instruction]
                else:
                    line_obj.executed_instruction = Instruction("exclude", None, None, None, None, line_obj.ref_executed_instruction, "Invalid")

            self.dump.append(line_obj)

        self.instructions = list(instructions_dict.values())
