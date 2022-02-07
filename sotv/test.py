import json
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor
from sotv.compile_utils import compile_program, compile_exec
from sotv.utils import save_score, compile_obf, execute_obfuscated_bench, execute_plain, run_score


def test_plain():
    executable_elf = os.path.join(folder, "test.out")

    input_list = os.listdir(input_folder)

    for inp in input_list:
        exec_params = [executable_elf, os.path.join(input_folder, inp)]
        trace = execute_plain(exec_params[0], compile_method=compile_program, args=exec_params[1:])
        save_score(run_score(trace), None, score_file, None, exec_params[1], None)


def test_bulk():
    executables_list = os.listdir(obfuscated_folder)
    input_list = os.listdir(input_folder)

    test_list = []

    try:
        already_computed = json.loads(open(score_file).read())
    except FileNotFoundError as e:
        already_computed = {}

    for executable in executables_list:
        for inp in input_list:
            obfuscation = executable[0:executable.rindex("_")]
            obfuscated_hash = executable[executable.rindex("_")+1:]
            if obfuscation in already_computed.keys():
                if obfuscated_hash in already_computed[obfuscation].keys():
                    if inp in already_computed[obfuscation][obfuscated_hash].keys():
                        continue
            if executable.endswith(".s") or executable.endswith(".txt"):
                continue
            test_list.append([os.path.join(obfuscated_folder, executable), os.path.join(input_folder, inp)])

    m = multiprocessing.Manager()
    lock = m.Lock()

    with ProcessPoolExecutor(max_workers=14) as executor:
        for obf_exec_params in test_list:
            obf_params = "_".join(obf_exec_params[0].split("_")[0:4])
            executor.submit(execute_multithreaded, obf_exec_params, score_file, obf_params, lock)

    return


def execute_multithreaded(obf_exec_params, name, obf_params, lock):
    print("Testing:", obf_exec_params)
    tid = int(multiprocessing.current_process().name.split("-")[-1])
    calc_and_save_score(execute_obfuscated_bench(obf_exec_params, thread_num=tid), name, obf_params, lock, obf_exec_params[1], obf_exec_params[0])


def calc_and_save_score(trace, name, obf_params, lock, input_md5, obf_md5):
    calc_score = run_score(trace[0])
    with lock:
        save_score(calc_score, trace[1], name, obf_params, input_md5, obf_md5)


def gen_compile():
    executable_elf = os.path.join(folder, "test.out")
    # compile_exec(source_file, executable_elf)

    #for k in range(9):
    #    compile_obf(source_file, (entry_point, 0, 0, 1, 1))
    #    print("1", k)
    # (rep_scramble (broken, always 0), rep_obfuscate, rep_garbage, heat_value (keep always 1))

    #for k in range(8):
    #    for i in range(10, 60, 10):
    #        compile_obf(source_file, (entry_point, 0, 0, i, 1))
    #        print("2", k, i)

    #for k in range(9):
    #    for i in range(1, 5):
    #        compile_obf(source_file, (entry_point, 0, i, 0, 1))
    #        print("3", k, i)

    #for k in range(9):
    #    for i in range(1, 4):
    #    compile_obf(source_file, (entry_point, 0, 5, 0, 1))
    #    print("4", k, 5)


if __name__ == "__main__":
    source_file = "./programSamples/sha256/sha256.c"
    score_file = "./scoreCalculator/results_bulk/sha256_scorefix.json"

    folder = os.path.dirname(source_file)
    obfuscated_folder = os.path.join(folder, "obfuscated")
    input_folder = os.path.join(folder, "inputs")
    entry_point = "main"

    #gen_compile()
    test_plain()
    test_bulk()
