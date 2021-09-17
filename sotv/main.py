import sys
from sys import argv
import utils
from sotv.EDG import offset_finder, edg
from sotv.Tracer.tracer import Tracer
from sotv.scoreCalculator.score import Metrics


def main():
    sys.setrecursionlimit(10**6)

    if len(argv) == 2:
        if argv[1] == "-h":
            print(f"Usage: {argv[0]} c_file")
            exit(1)
        else:
            print("#STARTING COMPILING STAGE#")
            utils.compile_asm(argv[1], "out.s")
            utils.compile_exec(argv[1], "a.out")
            utils.compile_asm_nosymbols(argv[1], "out_no_symbols.s")
            print("#RUNNING DUMP#")
            execution_dump = edg.edg(["a.out"])
            local_vars, global_vars = offset_finder.offset_finder("a.out")
            print("#EXECUTE TRACE#")
            tracer = Tracer(local_vars, global_vars, execution_dump)
            tracer.start_trace()
            metrics = Metrics(tracer)
            metrics.metric_score()

            print("\n\n\n\n")
            for dump_line in tracer.execution_dump.dump:
                try:
                    print(dump_line.executed_instruction.function_name.ljust(10," ")+dump_line.executed_instruction.readable.ljust(30," ") + "\t" + str(tracer.tracing_graph[dump_line]))
                except KeyError:
                    print(dump_line.executed_instruction.function_name.ljust(10," ")+dump_line.executed_instruction.readable.ljust(30," "))

            tracer.verify()
            input()
    else:
        print("Error in parameters (-h for help)")
        exit(1)


if __name__ == "__main__":
    main()
