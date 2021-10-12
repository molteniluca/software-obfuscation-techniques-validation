import gdb
import json
import os
import re

instr = "nop"


def dump_current():
    global instr

    dump_step = {"registers": {}, "SP_offsets": {}, "FP_offsets": {}, "var_values": {}}

    # Gets next executing instruction

    # Pretty print the next instruction pointed by the program counter
    if instr != "nop":
        dump_step["executed_instruction"] = instr[instr.index(">:") + 3:-1].replace("\t", " ")

        # Regex that searches the string between "<" and ">" (<function + offset>)
        dump_step["ref_executed_instruction"] = re.search('<(.+?)>', instr).group(1)
    else:
        dump_step["executed_instruction"] = None
        dump_step["ref_executed_instruction"] = None

    instr = gdb.execute("x/i $pc", to_string=True)

    # Dumps all registers
    for reg in regs:
        dump_step["registers"][reg] = int(gdb.parse_and_eval("$" + reg))

    for var in c_variables:
        try:
            # Computes the offset between the variable address and SP
            dump_step["SP_offsets"][var] = -int(gdb.parse_and_eval("$sp - (void *)&" + var))
        except gdb.error:
            pass
        try:
            # Computes the offset between the variable address and FP
            dump_step["FP_offsets"][var] = -int(gdb.parse_and_eval("$fp - (void *)&" + var))
        except gdb.error:
            pass
        try:
            # Gets the variable value
            dump_step["var_values"][var] = int(gdb.parse_and_eval(var))
        except gdb.error:
            pass

    return dump_step


def step_until_end_and_dump():
    global instr
    dump = []
    while True:
        if "<" + main_function in instr and "ret" in instr:
            dump.append(dump_current())
            break

        dump.append(dump_current())
        # Breaks only if it is in function start and next instruction is ret
        gdb.execute("stepi")  # Step to the next machine instruction

    return dump


def save_dump(dump):
    with open(dump_output, "w") as f:
        f.write(json.dumps(dump, indent=4))


def initialize_debug():
    # Imports in gdb the executable (For some reason qemu doesnt send this info trough gdbserver)
    gdb.execute("file " + exec_file)

    gdb.execute("target remote :1234")  # Connects to the qemu gdbserver

    gdb.execute("set pagination off")  # Avoid interruption for command result pagination in gdb

    gdb.execute("b *" + main_function)  # Sets a breakpoint at the function _start
    gdb.execute("continue")  # Continue until the breakpoint


# This shall be executed only by gdb
if __name__ == "__main__":
    config_file = open("EDG/tmp/EDG_conf.json", "r")
    config = config_file.read()
    config = json.loads(config)

    regs = config["registers"]
    main_function = config["main_function"]
    c_variables = config["c_variables"]
    dump_output = config["dump_file"]
    exec_file = config["exec_file"]

    initialize_debug()
    try:
        save_dump(step_until_end_and_dump())
    except Exception as e:
        os.system("rm " + dump_output)
        print("Failed debug")

    gdb.execute("quit")  # Exits gdb
