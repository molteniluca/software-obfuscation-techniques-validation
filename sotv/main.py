import json
import os
import sys
from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.Tracer.tracer import Tracer
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.scoreCalculator.score import Metrics
import time


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
                save_score(run_score(result), obf_params)
            else:
                save_score(run_score(result), None)
    else:
        print("Error in parameters (-h for help)")
        exit(1)


def compile_program(source_file, executable_elf, asm, destination_folder, O=0):
    print("# STARTING COMPILING STAGE #\n")
    try:
        utils.compile_exec(source_file, os.path.join(destination_folder, executable_elf), O=O)
        utils.compile_asm_nosymbols(source_file, os.path.join(destination_folder, asm))
    except SubProcessFailedException as e:
        print("Compilation failed")
        exit(-1)


def execute_obfuscated(source_file: str, obfuscator_params: (str, int, int), compile_method=compile_program, args=[]):
    sys.setrecursionlimit(10 ** 4)

    folder = os.path.dirname(source_file)
    obfuscated_elf = os.path.join(folder, "obf.out")
    obfuscated_asm = os.path.join(folder, "obf.s")
    asm = "out_no_symbols.s"
    asm_json = os.path.join(folder, "out_no_symbols.json")
    obf_exec_params = [obfuscated_elf] + args
    executable_elf = "test.out"

    compile_method(source_file, executable_elf, asm, folder)

    print("# RUNNING DUMP #\n")
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        try:
            utils.parse(os.path.join(folder, asm), asm_json)
            utils.obfuscate(asm_json, obfuscated_asm, *obfuscator_params)
            utils.compile_exec(obfuscated_asm, obfuscated_elf)
            try:
                obf_execution_dump = edg.edg(source_file + "_obf_" + str(obfuscator_params[1]) + "_" +
                                             str(obfuscator_params[2]), obf_exec_params, ignore_cache=True)
                obf_success = True
            except DumpFailedException as e:
                obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    print("#### " + str(obf_execution_dump))

    tracer = run_trace(obf_execution_dump, os.path.join(folder, executable_elf), trace_no_symbols=True)
    return tracer


def execute_plain(source_file: str, compile_method=compile_program, args=[]):
    sys.setrecursionlimit(10 ** 4)

    asm = "out_no_symbols.s"
    folder = os.path.dirname(source_file)
    executable_elf = os.path.join(folder, "test.out")

    compile_method(source_file, executable_elf)
    exec_params = [executable_elf] + args

    plain_execution_dump = run_dump(exec_params)
    tracer = run_trace(plain_execution_dump, executable_elf, trace_no_symbols=True)
    return tracer


def run_dump(exec_params, ignore_cache=True):
    print("# EXECUTE DUMP #")
    start_time = time.time()
    plain_execution_dump = edg.edg(exec_params[0], exec_params, ignore_cache=ignore_cache)
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
