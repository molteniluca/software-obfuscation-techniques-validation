import json
import os
import subprocess
import sys
from typing import Dict

from sotv import utils
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.EDG.execution_dump import ExecutionDump
from sotv.EDG.offset_finder import to_gdb_notation, offset_finder
from sotv.Tracer.instruction import Instruction

tmp_folder = "./EDG/tmp/"
dump_folder = "./EDG/dumps/"
config_file = "EDG_conf.json"


def edg(name: str, executable_params: list, ignore_cache: bool = False, timeout=900000,
        spawn_terminal=False, exclude=None) -> ExecutionDump:
    """
    This functions performs an execution and dumps data
    @param exclude: Methods to exclude from the trace
    @param spawn_terminal: Flag that if set makes the program run in a detached window
    @param timeout: Timeout in seconds in case the obfuscator creates an infinite loop
    @param ignore_cache: Ignore already executed dump in dumps folder
    @param name: name of the executed program
    @param executable_params: Argv, a list containing the executable name and parameters
    @return: An execution dump and a parsed instruction dictionary
    """

    if exclude is None:
        exclude = []
    else:
        print("Methods blacklist:" + " ".join(exclude))
    dump_file = dump_folder + name.split("/")[-1] + "_dump.json"

    config = {
        "registers": ["ra", "sp", "gp", "tp", "t0", "t1", "t2", "fp", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6",
                      "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6", "pc"],
        "main_function": "main",
        "c_variables": to_gdb_notation(*offset_finder(executable_params[0])),
        "dump_file": dump_file,
        "exec_file": executable_params[0]
    }

    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    if not os.path.isfile(dump_file) or ignore_cache:
        with open(tmp_folder + config_file, "w") as f:
            f.write(json.dumps(config))
        # Starts qemu session in background

        unix_sock_params = ["-g", "1234"]

        if spawn_terminal:
            exec_array = ["terminator", "-x", "timeout", str(timeout), "qemu-riscv64-static"] + unix_sock_params + executable_params
        else:
            exec_array = ["timeout", str(timeout), "qemu-riscv64-static", "-g", "1234"] + executable_params

        proc = subprocess.Popen(exec_array)
        subprocess.run(["gdb-multiarch", "-command=./EDG/edg_script.py", "-batch-silent"])
        proc.kill()

    try:
        dump = json.loads(open(dump_file, "r").read())
    except FileNotFoundError as e:
        raise DumpFailedException

    new_dump = []
    continuing = False
    for line in dump[1:]:
        cont = False
        for method in exclude:
            if method in line["ref_executed_instruction"]:
                cont |= True
                if not continuing:
                    new_dump.append({"ref_executed_instruction": method+"+exclude", "executed_instruction": line["executed_instruction"]})
                    continuing = True
        if cont:
            continue
        new_dump.append(line)

    dump = new_dump
    instructions = parse_instructions(dump)

    return ExecutionDump(instructions, dump)


def parse_instructions(dump) -> Dict[str, Instruction]:
    """
    This function parses the instructions contained in an execution dump
    @param dump: The execution dump
    @return: The dictionary in which the keys are the instruction ref and the values are the parsed instructions
    """


    code = ""
    for line in dump:

        if "ret" in line["executed_instruction"]:
            code += "jr ra" + "\n"
        else:
            code += line["executed_instruction"] + "\n"

    with open(tmp_folder + "instructions.asm", "w") as f:
        f.write(code)

    utils.parse(tmp_folder + "instructions.asm", tmp_folder + "parsed_instruction.json")

    parsed_file = open(tmp_folder + "parsed_instruction.json", "r")
    parsed = parsed_file.read()
    parsed = json.loads(parsed)

    instructions = {}
    for i in range(len(dump)):
        instructions[dump[i]["ref_executed_instruction"]] = Instruction(parsed[i]["opcode"],
                                                                            parsed[i]["r1"],
                                                                            parsed[i]["r2"],
                                                                            parsed[i]["r3"],
                                                                            parsed[i]["immediate"],
                                                                            dump[i]["ref_executed_instruction"],
                                                                            dump[i]["executed_instruction"])
    return instructions


if __name__ == "__main__":
    # Starts qemu session in background
    subprocess.Popen(["qemu-riscv64-static", "-g", "1234", "./a.out"])
    subprocess.Popen(["gdb-multiarch", "-command=edg_script.py"])
