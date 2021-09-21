import sys
from os import system
from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.Tracer.tracer import Tracer
from sotv.scoreCalculator.score import Metrics

tmp_folder = "./tmp/"


def main():
    sys.setrecursionlimit(10 ** 6)
    system("rm " + tmp_folder + "*")

    if len(argv) == 2 or len(argv) == 3:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} C_file/ASM_file [-t test obfuscated]")
            exit(1)
        else:
            test_obf = len(argv) == 3 and argv[2] == "-t"

            executable_elf = tmp_folder + "test.out"
            obfuscated_elf = tmp_folder + "obf.out"
            obfuscated_asm = tmp_folder + "obf.s"
            symbols_elf = tmp_folder + "test.out"
            asm = tmp_folder + "out_no_symbols.s"
            asm_json = tmp_folder + "out_no_symbols.json"
            exec_params = [executable_elf]
            obf_exec_params = [obfuscated_elf]

            print("# STARTING COMPILING STAGE #\n")
            utils.compile_exec(argv[1], executable_elf)
            utils.compile_asm_nosymbols(argv[1], asm)

            if test_obf:
                utils.parse(asm, asm_json)
                utils.obfuscate(asm_json, obfuscated_asm, 1, 1)
                utils.compile_exec(obfuscated_asm, obfuscated_elf)

            print("# RUNNING DUMP #\n")
            local_vars, global_vars = offset_finder.offset_finder(symbols_elf)
            dump_list = []
            plain_execution_dump = edg.edg(exec_params)
            dump_list.append(plain_execution_dump)

            if test_obf:
                obf_execution_dump = edg.edg(obf_exec_params)
                dump_list.append(obf_execution_dump)

            print("# EXECUTE TRACE #\n")
            for execution_dump in dump_list:
                print("#### " + str(execution_dump))
                tracer = Tracer(local_vars, global_vars, execution_dump)
                tracer.start_trace(trace_no_symbols=True)
                tracer.verify()

                metrics = Metrics(tracer)
                metrics.metric_score()

                tracer.print()
                print("\n" * 3)
    else:
        print("Error in parameters (-h for help)")
        exit(1)


if __name__ == "__main__":
    main()
