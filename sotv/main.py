from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.Tracer.tracer import Tracer


def main():
    if len(argv) == 2:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} c_file")
            exit(1)
        else:
            utils.compile_asm(argv[1], "out.s")
            utils.compile_exec(argv[1], "a.out")
            utils.compile_asm_nosymbols(argv[1], "out_no_symbols.s")
            execution_dump = edg.edg(["a.out"])
            tracer = Tracer(offset_finder.offset_finder("a.out"), execution_dump)
            tracer.start_trace()
    else:
        print("Error in parameters (-h for help)")
        exit(1)


if __name__ == "__main__":
    main()
