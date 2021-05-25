from pprint import pprint
from sys import argv
import utils
from sotv.EDG import offsetFinder, EDG


def main():
    if len(argv) == 2:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} c_file")
            exit(1)
        else:
            utils.compile_asm(argv[1], "out.s")
            utils.compile_exec(argv[1], "a.out")
            utils.compile_asm_nosymbols(argv[1], "out_no_symbols.s")
            pprint(offsetFinder.offset_finder(EDG.edg(["a.out"])))
    else:
        print("Error in parameters (-h for help)")
        exit(1)


if __name__ == "__main__":
    main()
