import gdb
import json
import re


def dump_current():
    dump_step = {"registers": {}, "SP_offsets": {}, "FP_offsets": {}}

    instr = gdb.execute("x/i $pc", to_string=True)

    # Pretty print the next instruction pointed by the program counter
    dump_step["next_instruction"] = instr[instr.index(">:") + 3:-1].replace("\t", " ")

    # Regex that searches the string between "<" and ">" (<function + offset>)
    dump_step["ref_next_instruction"] = re.search('<(.+?)>', instr).group(1)

    for reg in regs:
        dump_step["registers"][reg] = int(gdb.parse_and_eval("$" + reg))

    for var in c_variables:
        try:
            dump_step["SP_offsets"][var] = -int(gdb.parse_and_eval("$sp - (void *)&" + var))
        except gdb.error:
            dump_step["SP_offsets"][var] = None
        try:
            dump_step["FP_offsets"][var] = -int(gdb.parse_and_eval("$fp - (void *)&" + var))
        except gdb.error:
            dump_step["SP_offsets"][var] = None

    return dump_step


def step_until_end_and_dump():
    dump = []
    while True:
        dump.append(dump_current())
        instr = gdb.execute("x/i $pc", to_string=True)
        # Breaks only if it is in function start and next instruction is ret
        if "<" + main_function in instr and "ret" in instr:
            break
        gdb.execute("stepi")  # Step to the next machine instruction

    return dump


def save_dump(dump):
    with open(dump_output, "w") as f:
        f.write(json.dumps(dump, indent=4))


def initialize_debug():
    # Imports in gdb the executable (For some reason qemu doesnt send this info trough gdbserver)
    gdb.execute("file a.out")

    gdb.execute("target remote :1234")  # Connects to the qemu gdbserver

    gdb.execute("set pagination off")  # Avoid interruption for command result pagination in gdb

    gdb.execute("b *" + main_function)  # Sets a breakpoint at the function _start
    gdb.execute("continue")  # Continue until the breakpoint


if __name__ == "__main__":
    config_file = open("EDG/EDG_conf.json", "r")
    config = config_file.read()
    config = json.loads(config)

    regs = config["registers"]
    main_function = config["main_function"]
    c_variables = config["c_variables"]
    dump_output = config["dump_file"]
    exec_file = config["exec_file"]

    initialize_debug()
    save_dump(step_until_end_and_dump())

    gdb.execute("quit")  # Exits gdb
