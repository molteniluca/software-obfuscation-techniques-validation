import json
import subprocess
from typing import Tuple, Dict
from sotv.EDG.offset_finder import to_gdb_notation, offset_finder
from sotv.Tracer.instruction import Instruction

tmp_folder = "./EDG/tmp/"

dump_file = "dump.json"
config_file = "EDG_conf.json"


def edg(executable_params: list) -> Tuple[object, Dict[str, Instruction]]:
    """
    This functions performs an execution and dumps data
    @param executable_params: Argv, a list containing the executable name and parameters
    @return: An execution dump and a parsed instruction dictionary
    """

    config = {
        "registers": ["ra", "sp", "gp", "tp", "t0", "t1", "t2", "fp", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6",
                      "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6", "pc"],
        "main_function": "main",
        "c_variables": to_gdb_notation(*offset_finder(executable_params[0])),
        "dump_file": tmp_folder + dump_file,
        "exec_file": executable_params[0]
    }

    with open(tmp_folder + config_file, "w") as f:
        f.write(json.dumps(config))

    # Starts qemu session in background
    subprocess.Popen(["qemu-riscv64-static", "-g", "1234"] + executable_params)
    subprocess.run(["gdb-multiarch", "-command=./EDG/EDG_script.py", "-batch-silent"])

    dump = json.loads(open(tmp_folder + dump_file, "r").read())

    instructions = parse_instructions(dump)

    return dump, instructions


def parse_instructions(dump) -> Dict[str, Instruction]:
    """
    This function parses the instructions contained in an execution dump
    @param dump: The execution dump
    @return: The dictionary in which the keys are the instruction ref and the values are the parsed instructions
    """
    code = ""
    for line in dump:
        if "ret" in line["next_instruction"]:
            code += "jr ra" + "\n"
        else:
            code += line["next_instruction"] + "\n"

    with open(tmp_folder + "instructions.asm", "w") as f:
        f.write(code)

    subprocess.run(["./EDG/parser", tmp_folder + "instructions.asm", tmp_folder + "parsed_instruction.json"])

    parsed_file = open(tmp_folder + "parsed_instruction.json", "r")
    parsed = parsed_file.read()
    parsed = json.loads(parsed)

    instructions = {}
    for i in range(len(dump)):
        instructions[dump[i]["ref_next_instruction"]] = Instruction(parsed[i]["opcode"],
                                                                    parsed[i]["r1"],
                                                                    parsed[i]["r2"],
                                                                    parsed[i]["r3"],
                                                                    parsed[i]["immediate"])
    return instructions


if __name__ == "__main__":
    # Starts qemu session in background
    subprocess.Popen(["qemu-riscv64-static", "-g", "1234", "./a.out"])
    subprocess.run(["gdb-multiarch", "-command=EDG_script.py", "-batch-silent"])
