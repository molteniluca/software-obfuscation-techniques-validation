import sys
from os import system
from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.Tracer.tracer import Tracer
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.scoreCalculator.score import Metrics

tmp_folder = "./tmp/"


def main():
    if len(argv) == 2 or len(argv) == 3:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} C_file/ASM_file [-t test obfuscated]")
            exit(1)
        else:
            test_obf = len(argv) == 3 and argv[2] == "-t"
            if test_obf:
                result = execute_obfuscated(argv[1], ("main", 5, 5))
            else:
                result = execute_plain(argv[1])

            result[0].print()
            result[1].print()
    else:
        print("Error in parameters (-h for help)")
        exit(1)


def execute_obfuscated(source_file: str, obfuscator_params: (str, int, int)):
    sys.setrecursionlimit(10 ** 6)
    system("rm " + tmp_folder + "*")

    obfuscated_elf = tmp_folder + "obf.out"
    obfuscated_asm = tmp_folder + "obf.s"
    symbols_elf = tmp_folder + "test.out"
    asm = tmp_folder + "out_no_symbols.s"
    asm_json = tmp_folder + "out_no_symbols.json"
    obf_exec_params = [obfuscated_elf]
    executable_elf = tmp_folder + "test.out"

    print("# STARTING COMPILING STAGE #\n")
    try:
        if source_file[-len(".json"):] == ".json":
            utils.obfuscate(argv[1], asm, "main", 0, 0)
            utils.compile_exec(asm, executable_elf)
        else:
            utils.compile_exec(argv[1], executable_elf)
            utils.compile_asm_nosymbols(argv[1], asm)
    except SubProcessFailedException as e:
        print("Compilation failed")
        exit(-1)

    obf_success = False
    i = 0
    while not obf_success:
        i += 1
        try:
            utils.parse(asm, asm_json)
            utils.obfuscate(asm_json, obfuscated_asm, *obfuscator_params)
            utils.compile_exec(obfuscated_asm, obfuscated_elf)
            try:
                obf_execution_dump = edg.edg(obf_exec_params)
                obf_success = True
            except DumpFailedException as e:
                obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    local_vars, global_vars = offset_finder.offset_finder(symbols_elf)

    print("#### " + str(obf_execution_dump))
    tracer = Tracer(local_vars, global_vars, obf_execution_dump)
    tracer.start_trace(trace_no_symbols=True)

    metrics = Metrics(tracer)
    metrics.metric_score()

    return tracer, metrics


def execute_plain(source_file: str):
    sys.setrecursionlimit(10 ** 6)
    system("rm " + tmp_folder + "*")

    executable_elf = tmp_folder + "test.out"
    symbols_elf = tmp_folder + "test.out"
    asm = tmp_folder + "out_no_symbols.s"
    exec_params = [executable_elf]

    print("# STARTING COMPILING STAGE #\n")
    try:
        if source_file[-len(".json"):] == ".json":
            utils.obfuscate(argv[1], asm, "main", 0, 0)
            utils.compile_exec(asm, executable_elf)
        else:
            utils.compile_exec(argv[1], executable_elf)
            utils.compile_asm_nosymbols(argv[1], asm)
    except SubProcessFailedException as e:
        print("Compilation failed")
        exit(-1)

    print("# RUNNING DUMP #\n")
    local_vars, global_vars = offset_finder.offset_finder(symbols_elf)
    plain_execution_dump = edg.edg(exec_params)

    print("# EXECUTE TRACE #\n")

    print("#### " + str(plain_execution_dump))
    tracer = Tracer(local_vars, global_vars, plain_execution_dump)
    tracer.start_trace(trace_no_symbols=True)

    metrics = Metrics(tracer)
    metrics.metric_score()

    return tracer, metrics


if __name__ == "__main__":
    main()
