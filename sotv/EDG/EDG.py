import json
import re
from os import system
from pygdbmi.gdbcontroller import GdbController


gdbmi = {}

def dumpCurrent():
    dump = {}
    dump["registers"] = {}

    instr = gdbmi.write("x/i $pc")[1]["payload"]

    # Pretty print the next instruction pointed by the program counter
    dump["instruction"] = instr[instr.index(">:") + 3:-1].replace("\t", " ")
    arr=[]
    for i in range(33):
        arr.append(i)

    dump["registers"][regs[i]] = gdbmi.write("-data-list-register-names " + str(arr))

    return dump


def stepUntilEndAndDump(mainFunction):
    dump = {}
    while True:
        instr = gdbmi.write("x/i $pc")
        # Regex that searches the string between "<" and ">" (<function + offset>)
        instr = instr[1]["payload"]
        print(instr)
        line = re.search('<(.+?)>', instr).group(1)
        dump[line] = dumpCurrent()

        # Breaks only if it is in function start and next instruction is ret
        if "<" + mainFunction in instr and "ret" in instr:
            break
        gdbmi.write("stepi")  # Step to the next machine instruction

    return dump


def saveToFile(dump):
    with open("dump.json", "w") as f:
        f.write(json.dumps(dump))


def initializeDebug(mainFunction):
    system("qemu-riscv64-static -g 1234 ./a.out &")  # Starts qemu session in background
    # Imports in gdb the executable (For some reason qemu doesnt send this info trough gdbserver)
    gdbmi.write("file a.out")

    gdbmi.write("target remote :1234")  # Connects to the qemu gdbserver

    gdbmi.write("b *" + mainFunction)  # Sets a breakpoint at the function _start
    gdbmi.write("continue")  # Continue until the breakpoint


if __name__ == "__main__":
    config_file = open("EDG_conf.json", "r")
    config = config_file.read()
    config = json.loads(config)

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi3"],time_to_check_for_additional_output_sec=0.01)

    initializeDebug(config["mainFunction"])
    regs=gdbmi.write("-data-list-register-names")[0]["payload"]["register-names"][0:33]

    dump = stepUntilEndAndDump(config["mainFunction"])

    saveToFile(dump)
    gdbmi.write("quit")  # Exits gdb

