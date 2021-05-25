import gdb
import json
import re


def dumpCurrent():
    dump = {}
    dump["registers"] = {}

    instr = gdb.execute("x/i $pc", to_string=True)

    # Pretty print the next instruction pointed by the program counter
    dump["instruction"] = instr[instr.index(">:") + 3:-1].replace("\t", " ")

    # Regex that searches the string between "<" and ">" (<function + offset>)
    dump["refInstruction"] = re.search('<(.+?)>', instr).group(1)

    for reg in regs:
        dump["registers"][reg] = int(gdb.parse_and_eval("$" + reg))

    return dump


def stepUntilEndAndDump(mainFunction):
    dump = []
    while True:
        dump.append(dumpCurrent())
        instr = gdb.execute("x/i $pc", to_string=True)
        # Breaks only if it is in function start and next instruction is ret
        if "<" + mainFunction in instr and "ret" in instr:
            break
        gdb.execute("stepi")  # Step to the next machine instruction

    return dump

def saveToFile(dump):
    with open("dump.json", "w") as f:
        f.write(json.dumps(dump, indent=4))


def initializeDebug(mainFunction):
    # Imports in gdb the executable (For some reason qemu doesnt send this info trough gdbserver)
    gdb.execute("file a.out")

    gdb.execute("target remote :1234")  # Connects to the qemu gdbserver

    gdb.execute("set pagination off")  # Avoid interruption for command result pagination in gdb

    gdb.execute("b *" + mainFunction)  # Sets a breakpoint at the function _start
    gdb.execute("continue")  # Continue until the breakpoint


if __name__ == "__main__":
    config_file = open("EDG_conf.json", "r")
    config = config_file.read()
    config = json.loads(config)

    regs = config["registers"]
    initializeDebug(config["mainFunction"])

    dump = stepUntilEndAndDump(config["mainFunction"])

    saveToFile(dump)
    gdb.execute("quit")  # Exits gdb
