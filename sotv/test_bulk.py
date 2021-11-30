import os
from sotv.main import execute_obfuscated, compile_program, execute_plain
from sotv.programSamples.New_Patricia.compile_patricia import compile_program_patricia

program_folder = "./programSamples"


def test_bulk():
    program_list = [
        ("bubbleSort/bubblesort_old.c", compile_program, []),
        ("patricia_test.c", compile_program_patricia, ["small.udp"])
    ]

    test_list = [
        None,
        ("main", 1, 1),
        ("main", 2, 2)
    ]

    trace_dict = {}

    for program in program_list:
        for test in test_list:
            trace_dict[(program[0], test)] = exec_test(os.path.join(program_folder, program[0]),
                                                       program[1],
                                                       test,
                                                       program[2]
                                                       )

    return trace_dict


def exec_test(program, compile_method, test, args):
    if test is None:
        return execute_plain(program, compile_method=compile_method, args=args)
    else:
        return execute_obfuscated(program, test, compile_method=compile_method, args=args)


if __name__ == "__main__":
    test_bulk()
