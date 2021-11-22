import json
import os
import sys
from os import system
from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.Tracer.tracer import Tracer
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.scoreCalculator.score import Metrics
import time

tmp_folder = "./tmp/"


def main():
    obf_params = ("main", 1, 1)

    if len(argv) == 2 or len(argv) == 3:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} C_file/ASM_file [-t test obfuscated]")
            exit(1)
        else:
            test_obf = len(argv) == 3 and argv[2] == "-t"
            if test_obf:
                result = execute_obfuscated(argv[1], obf_params)
            else:
                result = execute_plain(argv[1])

            if test_obf:
                save_score(result[1], obf_params)
            else:
                save_score(result[1], None)

            result[1].print()
    else:
        print("Error in parameters (-h for help)")
        exit(1)


def execute_obfuscated(source_file: str, obfuscator_params: (str, int, int)):
    sys.setrecursionlimit(10 ** 4)
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

    print("# RUNNING DUMP #\n")
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        try:
            utils.parse(asm, asm_json)
            utils.obfuscate(asm_json, obfuscated_asm, *obfuscator_params)
            utils.compile_exec(obfuscated_asm, obfuscated_elf)
            try:
                obf_execution_dump = edg.edg(argv[1] + "_obf_" + str(obfuscator_params[1]) + "_" + str(obfuscator_params[2]), obf_exec_params, ignore_cache=False)
                obf_success = True
            except DumpFailedException as e:
                obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    print("#### " + str(obf_execution_dump))

    tracer = run_trace(obf_execution_dump, symbols_elf, trace_no_symbols=True)
    return tracer, run_score(tracer)


def execute_plain(source_file: str):
    sys.setrecursionlimit(10 ** 4)
    system("rm " + tmp_folder + "*")

    executable_elf = tmp_folder + "test.out"
    symbols_elf = tmp_folder + "test.out"
    asm = tmp_folder + "out_no_symbols.s"

    print("# STARTING COMPILING STAGE #\n")
    try:
        if source_file[-len(".json"):] == ".json":
            exec_params = [executable_elf]
            utils.obfuscate(argv[1], asm, "main", 0, 0)
            utils.compile_exec(asm, executable_elf)
        else:
            # Test Purpose
            if source_file == './programSamples/New_Patricia/patricia_test.c':
                path = "./programSamples/New_Patricia/"
                exec_params = [executable_elf, "./programSamples/New_Patricia/small.udp"]
                utils.compile_lib_patricia()
                utils.compile_patricia(argv[1], executable_elf, path)
                utils.compile_patricia_nosymbols(argv[1], asm, path)
            else:
                exec_params = [executable_elf]
                utils.compile_exec(argv[1], executable_elf)
                utils.compile_asm_nosymbols(argv[1], asm)
    except SubProcessFailedException as e:
        print("Compilation failed")
        exit(-1)

    plain_execution_dump = run_dump(exec_params)
    tracer = run_trace(plain_execution_dump, symbols_elf, trace_no_symbols=True)
    return tracer, run_score(tracer)


def run_dump(exec_params, ignore_cache=False):
    print("# EXECUTE DUMP #")
    start_time = time.time()
    plain_execution_dump = edg.edg(argv[1], exec_params, ignore_cache=ignore_cache)
    print("--- %s seconds ---" % (time.time() - start_time))
    return plain_execution_dump


def run_trace(plain_execution_dump, symbols_elf, trace_no_symbols=True):
    print("# EXECUTE TRACE #\n")
    start_time = time.time()
    local_vars, global_vars = offset_finder.offset_finder(symbols_elf)
    tracer = Tracer(local_vars, global_vars, plain_execution_dump)
    tracer.start_trace(trace_no_symbols=trace_no_symbols)
    tracer.print()
    print("--- %s seconds ---" % (time.time() - start_time))
    return tracer


def run_score(tracer):
    print("# CALCULATE SCORE #")
    start_time = time.time()
    metrics = Metrics(tracer)
    metrics.metric_score()
    print("--- %s seconds ---" % (time.time() - start_time))
    return metrics


score_path = "./scoreCalculator/results/"


def save_score(score, obf):
    filename = score_path + argv[1].split("/")[-1]

    filename += ".json"

    if os.path.isfile(filename):
        result = json.loads(open(filename, "r").read())
    else:
        result = {}

    if obf is not None:
        if str(obf[1]) + "_" + str(obf[2]) not in result.keys():
            result[str(obf[1]) + "_" + str(obf[2])] = []
        result[str(obf[1]) + "_" + str(obf[2])].append(score.get_dict())
    else:
        result["plain"] = score.get_dict()

    with open(filename, "w") as f:
        f.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
