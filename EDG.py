import gdb
from os import system
import json
import re

riscv64_regs = ["ra", "sp", "gp", "tp", "t0", "t1", "t2", "fp", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6", "pc"]
c_vars = ["_start::a","fun2::b"]

def dumpCurrent():
    dump = {}
    dump["registers"] = {}
    dump["c_variables"] = {}

    instr = gdb.execute("x/i $pc", to_string=True)
    dump["instruction"] = instr[instr.index(">:")+3:-1].replace("\t"," ") #Pretty print the next instruction pointed by the program counter

    for var in c_vars:
        try:
            dump["c_variables"][var] = hex(gdb.parse_and_eval(var))
        except:
            pass # If the function isn't already called the above command will trigger an exception

    for reg in riscv64_regs:
        dump["registers"][reg] = hex(gdb.parse_and_eval("$"+reg))

    return dump


def stepUntilEndAndDump():
    dump = {}

    while(True):
        instr = gdb.execute("x/i $pc", to_string=True)
        line = re.search('<(.+?)>', instr).group(1)  # Regex that searches the string between "<" and ">" (<function + offset>)
        dump[line] = dumpCurrent()
        if("<_start" in instr and "ret" in instr): # Breaks only if it is in function start and next instruction is ret
            break
        gdb.execute("stepi") # Step to the next machine instruction

    return dump


def saveToFile(dump):
    with open("dump.json","w") as f:
        f.write(json.dumps(dump,indent=4)) #Pretty print the json


def initializeDebug():
    system("riscv64-linux-gnu-gcc -g prova.c -nostartfiles")
    system("qemu-riscv64-static -g 1234 ./a.out &") # Starts qemu session in background

    gdb.execute("file a.out") # Imports in gdb the executable (For some reason qemu doesnt send this info trough gdbserver)
    gdb.execute("target remote :1234") # Connects to the qemu gdbserver

    gdb.execute("set pagination off") # Avoid interruption for command result pagination in gdb

    gdb.execute("b *_start")  # Sets a breakpoint at the function _start
    gdb.execute("continue") # Continue until the breakpoint




initializeDebug()

dump = stepUntilEndAndDump()
saveToFile(dump)
gdb.execute("quit") # Exits gdb
