import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor

from sotv import utils
from sotv.compile_utils import compile_program, compile_exec
from sotv.utils import save_score, compile_obf, execute_obfuscated_bench, execute_plain, run_score

program_folder = "./programSamples"


def test_plain():
    folder = "./programSamples/sha256/"
    executable_elf = os.path.join(folder, "test.out")

    input_list = os.listdir("./programSamples/sha256/inputs/")

    for inp in input_list:
        exec_params = [executable_elf, "./programSamples/sha256/inputs/" + inp]
        trace = execute_plain(exec_params[0], compile_method=compile_program, args=exec_params[1:])
        save_score(run_score(trace), None, "sha256", None, exec_params[1], None)


def test_bulk():
    # (Path, entry point, compile_suite, args)
    program_list = [
        ("sha256/sha256.c", "main", (utils.compile_exec, compile_obf), []),
    ]

    executables_list = os.listdir("./programSamples/sha256/obfuscated/")
    input_list = os.listdir("./programSamples/sha256/inputs/")

    test_list = []

    for executable in executables_list:
        for inp in input_list:
            test_list.append(["./programSamples/sha256/obfuscated/" + executable, "./programSamples/sha256/inputs/" + inp])

    m = multiprocessing.Manager()
    lock = m.Lock()

    with ProcessPoolExecutor(max_workers=4) as executor:
        for obf_exec_params in test_list:
            print("Testing:", obf_exec_params)
            obf_params = "_".join(obf_exec_params[0].split("_")[0:4])
            executor.submit(execute_multithreaded, obf_exec_params, "sha256", obf_params, lock)

    return


def execute_multithreaded(obf_exec_params, name, obf_params, lock):
    id = int(multiprocessing.current_process().name.split("-")[-1])
    calc_and_save_score(execute_obfuscated_bench(obf_exec_params, thread_num=id), name, obf_params, lock, obf_exec_params[1], obf_exec_params[0])


def calc_and_save_score(trace, name, obf_params, lock, input_md5, obf_md5):
    calc_score = run_score(trace[0])
    with lock:
        save_score(calc_score, trace[1], name, obf_params, input_md5, obf_md5)


def gen_compile():
    source_file = "./programSamples/sha256/sha256.c"
    folder = os.path.dirname(source_file)
    executable_elf = os.path.join(folder, "test.out")
    compile_exec(source_file, executable_elf)
    # (rep_scramble (broken, always 0), rep_obfuscate, rep_garbage, heat_value (keep always 1))
    compile_obf("./programSamples/sha256/sha256.c", ("main", 0, 0, 1, 1))
    for i in range(10, 90, 10):
        compile_obf("./programSamples/sha256/sha256.c", ("main", 0, 0, i, 1))


if __name__ == "__main__":
    #gen_compile()
    #test_plain()
    test_bulk()
