import json
import os
import sys

from sotv import utils
from sotv.EDG import edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.main import compile_program, execute_plain, run_trace, run_score

program_folder = "./programSamples"
score_path = "./scoreCalculator/results_bulk/"


def save_score(score_calc, score, name, obf):
    exp_name = score_path + os.path.basename(name) + ".json"

    if os.path.isfile(exp_name):
        result = json.loads(open(exp_name, "r").read())
    else:
        result = {}

    if obf is not None:
        if str(obf) not in result.keys():
            result[str(obf)] = []
        result[str(obf)].append({"calc": score_calc.get_dict(), "DETON": score})
    else:
        result["plain"] = score_calc.get_dict()

    with open(exp_name, "w") as f:
        f.write(json.dumps(result, indent=4))


def test_bulk():
    obfuscated_folder = "./programSamples/benchmark_output"

    program_list = [
        ("bubbleSort/bubblesort_old.c", compile_program, [])
    ]

    test_list = [
        None,
        ("main", 20, 20, 20, 20)
    ]

    trace_dict = {}

    for program in program_list:
        for test in test_list:
            trace_dict[(program[0], test)] = exec_test(os.path.join(program_folder, program[0]),
                                                       program[1],
                                                       test,
                                                       program[2]
                                                       )

    for key in trace_dict.keys():
        name, test = key
        calc_score = run_score(trace_dict[key][0])

        save_score(calc_score, trace_dict[key][1], name, test)

    return trace_dict


def execute_obfuscated_bench(source_file: str, obfuscator_params: (str, int, int), compile_method=compile_program, args=[]):
    sys.setrecursionlimit(10 ** 4)

    folder = os.path.dirname(source_file)
    obfuscated_elf = os.path.join(folder, "obf.out")
    asm = "out_no_symbols.s"
    obfuscated_asm = os.path.join(folder, "out_no_symbols.s")
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
            utils.obfuscate_bench(asm_json, *obfuscator_params)
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

    score = {}
    with open(asm_json + "_metrics.txt", "r") as f:
        for line in f:
            key_line, value = line.split(":")
            score[key_line] = json.loads(value.split("->")[0])

    return tracer, score


def exec_test(program, compile_method, test, args):
    if test is None:
        return execute_plain(program, compile_method=compile_method, args=args), None
    else:
        trace_obfuscated = execute_obfuscated_bench(program, test, compile_method=compile_method, args=args)
        return trace_obfuscated


if __name__ == "__main__":
    test_bulk()
