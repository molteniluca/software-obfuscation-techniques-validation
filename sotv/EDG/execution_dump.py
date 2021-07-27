class DumpLine:
    registers: dict
    SP_offsets: dict
    FP_offsets: dict
    var_values: dict
    next_instruction: str
    ref_next_instruction: str

    def __init__(self, line):
        self.__dict__ = line


class ExecutionDump:
    instructions: dict
    dump: list = []

    def __init__(self, instructions, dump):
        self.instructions = instructions
        for line in dump:
            cos = DumpLine(line)
            self.dump.append(cos)
