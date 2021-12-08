import gdb
import json
import os

old_instr = "nop"
old_instr_name = "nop"
old_instr_pc = 0


def dump_current():
    global old_instr
    global old_instr_pc
    global old_instr_name

    dump_step = {"registers": {}, "SP_offsets": {}, "FP_offsets": {}, "var_values": {}}

    # Gets next executing instruction

    # Pretty print the next instruction pointed by the program counter
    if old_instr_pc != 0:
        dump_step["executed_instruction"] = old_instr
        dump_step["ref_executed_instruction"] = old_instr_name + "+" + str(old_instr_pc)
    else:
        dump_step["executed_instruction"] = None
        dump_step["ref_executed_instruction"] = None

    # Dumps all registers
    for reg in regs:
        dump_step["registers"][reg] = int(gdb.parse_and_eval("$" + reg))

    return dump_step


def step_until_end_and_dump():
    global old_instr
    global old_instr_name
    global old_instr_pc
    end_dump = False
    dump = []
    while True:
        if end_dump:
            break
        '''try:
            while "None" in str(gdb.find_pc_line(old_instr_pc).symtab) and old_instr_pc != 0:
                frame = gdb.selected_frame()
                old_instr_name = frame.name()
                old_instr_pc = frame.pc()
                old_instr = frame.architecture().disassemble(old_instr_pc, old_instr_pc)[0]["asm"]
                gdb.execute("ni")
        except gdb.error as e:
            return dump '''
        dump.append(dump_current())
        frame = gdb.selected_frame()
        old_instr_name = frame.name()
        old_instr_pc = frame.pc()
        old_instr = frame.architecture().disassemble(old_instr_pc, old_instr_pc)[0]["asm"]
        # Breaks only if it is in function start and next instruction is ret
        if "ret" in old_instr and old_instr_name == "main":
            end_dump = True
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
