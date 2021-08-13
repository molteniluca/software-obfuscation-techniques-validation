from sotv.Tracer.instruction_adapter import AdapterInterface
from sotv.Tracer.structures import opcodes, registers


class Instruction:
    """
    Define instruction structure

    opcode -- the opcode of the instruction
    r1 -- first register
    r2 -- second register
    r3 -- third register
    immediate -- immediate if needed
    function_name -- the function name
    offset -- the offset from the start of the function
    """

    function_name: str
    offset: int
    opcode: opcodes
    r1: registers
    r2: registers
    r3: registers
    immediate: int
    ins_adapter: AdapterInterface

    def __init__(self, opcode, r1, r2, r3, immediate, ref):
        self.opcode = opcode
        self.ins_adapter = AdapterInterface()
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.immediate = immediate
        self.function_name = ref.split("+")[0]
        try:
            self.offset = ref.split("+")[1]
        except IndexError:
            self.offset = 0

    def modified_register(self):
        if self.opcode[1]:
            return self.r1
        else:
            return None

    def ref_str(self):
        if self.offset != 0:
            return self.function_name+"+"+str(self.offset)
        else:
            return self.function_name
