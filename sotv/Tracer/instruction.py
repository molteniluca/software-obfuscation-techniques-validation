from structures import registers, opcodes


class Instruction:
    """
    Define instruction structure

    index -- a int that indicate at what row is executed the instruction
    opcode -- the opcode of the instruction
    r1 -- first register
    r2 -- second register
    r3 -- third register
    immediate -- immediate if needed
    """
    index: int
    opcode: opcodes
    r1: registers
    r2: registers
    r3: registers
    immediate: int

    def __init__(self, index, opcode, r1, r2, r3, immediate):
        self.index = index
        self.opcode = opcode
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.immediate = immediate

    def modified_register(self):
        return self.r1
