import json
import multiprocessing
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from sotv import utils
from sotv.EDG import edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.main import compile_program, execute_plain, run_trace, run_score
from sotv.programSamples.New_Susan.compile_susan import compile_program_susan
from sotv.programSamples.New_Patricia.compile_patricia import compile_program_patricia, compile_obf_patricia
from sotv.utils import compile_asm_nosymbols, obfuscate_bench, parse, compile_exec

program_folder = "./programSamples"
score_path = "./scoreCalculator/results_bulk/"


def test_bulk():
    obfuscated_folder = "./programSamples/benchmark_output"

    # (Path, entry point, compile_suite, args)
    program_list = [
        #("bubbleSort/bubblesort_old.c", "main", (utils.compile_exec, compile_obf), []),
        # ("dijkstra/dijkstra.c", compile_program, []),
        # ("fibonacci/fibonacci.c", compile_program, []),
        # ("New_CRC/crc_32_old.c", compile_program, []),
        # ("quickSort/quickSort.c", compile_program, []),
        # ("New_Susan/susan.c", compile_program_susan, ["input_small.pgm"]),
        ("New_Patricia/patricia_test.c", "bit", (compile_program_patricia, compile_obf_patricia), ["./programSamples/New_Patricia/small.udp"])
    ]

    test_list = [
        #None,
        (1,1,1,1)
    ]

    m = multiprocessing.Manager()
    lock = m.Lock()

    with ProcessPoolExecutor(max_workers=12) as executor:

        for program in program_list:
            for test in test_list:
                print("Testing:", program, test)

                trace = exec_test(program, test)
                executor.submit(calc_and_save_score, trace, program[0], test, lock)
    return


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
        result["plain"] = [{}]
        result["plain"][0]["calc"] = score_calc.get_dict()

    with open(exp_name, "w") as f:
        f.write(json.dumps(result, indent=4))


def calc_and_save_score(trace, name, test, lock):
    calc_score = run_score(trace[0])
    with lock:
        save_score(calc_score, trace[1], name, test)


def exec_test(program, test):
    # (Path, entry point, compile_suite, args)
    if test is None:
        return execute_plain(os.path.join(program_folder, program[0]), compile_method=program[2][0], args=program[3]),\
               None
    else:
        return execute_obfuscated_bench(os.path.join(program_folder, program[0]),
                                        (program[1], *test),
                                        compile_method=program[2][1],
                                        args=program[3])


def compile_obf(input_path, output_path, obfuscator_params, obf_exec_params, O = 0):
    folder = os.path.dirname(input_path)
    obfuscated_asm = os.path.join(folder, "obf.s")
    asm = os.path.join(folder, "out_no_symbols.s")
    asm_json = os.path.join(folder, "out_no_symbols.json")
    compile_asm_nosymbols(input_path, asm, O=O)
    parse(asm, asm_json)
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        try:
            obfuscate_bench(asm_json, *obfuscator_params)
            os.rename(asm_json+".s", obfuscated_asm)
            compile_exec(obfuscated_asm, output_path)
            try:
                obf_execution_dump = edg.edg(os.path.basename(input_path) + "_last_obf", obf_exec_params, ignore_cache=True)
                obf_success = True
            except DumpFailedException as e:
                obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    return obf_execution_dump


def execute_obfuscated_bench(source_file: str, obfuscator_params, compile_method=compile_program, args=None):
    if args is None:
        args = []
    sys.setrecursionlimit(10 ** 4)

    folder = os.path.dirname(source_file)
    obfuscated_elf = os.path.join(folder, "obf.out")

    executable_elf = "test.out"
    obf_exec_params = [obfuscated_elf] + args

    obf_execution_dump = compile_method(source_file, obfuscated_elf, obfuscator_params, obf_exec_params)

    tracer = run_trace(obf_execution_dump, os.path.join(folder, executable_elf), trace_no_symbols=True)

    score = {}
    with open(os.path.join(folder, "out_no_symbols.json_metrics.txt"), "r") as f:
        for line in f:
            key_line, value = line.split(":")
            score[key_line] = json.loads(value.split("->")[0])

    return tracer, score


if __name__ == "__main__":
    test_bulk()
