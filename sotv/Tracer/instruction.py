from sotv.Tracer.structures import opcodes, registers
from sotv.Tracer.instruction_adapter import AdapterInterface


class Instruction:
    """
    Define instruction structure

    opcode -- the opcode of the instruction
    r1 -- first register
    r2 -- second register
    r3 -- third register
    immediate -- immediate if needed
    ins_adapter -- strategy to apply for this type of instruction
    """
    opcode: opcodes
    r1: registers
    r2: registers
    r3: registers
    immediate: int
    ins_adapter: AdapterInterface

    def __init__(self, opcode, r1, r2, r3, immediate):
        self.opcode = opcode
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.immediate = immediate

    def modified_register(self):
        if self.opcode[1]:
            return self.r1
        else:
            return None
