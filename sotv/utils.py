import hashlib
import json
import os
import subprocess
import sys
import time

from sotv.EDG import edg, offset_finder
from sotv.Tracer.tracer import Tracer
from sotv.compile_utils import compile_asm_nosymbols, parse, obfuscate_bench, compile_exec, compile_program
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.scoreCalculator.score import Metrics

score_path = "./scoreCalculator/results_bulk/"


# {"1_1_1_1":
#   {"obfmd5":
#       {"inputmd5":[]
#       }
#   }
#  "plain":{
#   {"inputmd5":{}
#       }
#  }
# }

def save_score(calc_score, DETON_score, name, obf_params, input_md5, obf_md5):
    exp_name = score_path + os.path.basename(name) + ".json"

    input_md5 = os.path.basename(input_md5)[-32:]

    if os.path.isfile(exp_name):
        result = json.loads(open(exp_name, "r").read())
    else:
        result = {}

    if obf_params is not None:
        obf_params = obf_params.split("/")[-1]
        obf_md5 = os.path.basename(obf_md5)[-32:]
        plain_score = {"mean_heat": DETON_score["Mean heat before"],
                       "executed_instructions": DETON_score["Executed instructions before"]
                       }
        obf_score = {"mean_heat": DETON_score["Mean heat after"],
                     "executed_instructions": DETON_score["Executed instructions after"],
                     "mean_fragmentation": DETON_score["Mean fragmentation"],
                     "number_of_original_ValueBlock": DETON_score["Number of original ValueBlock"],
                     "list_of_fragmented_ValueBlock": DETON_score["List of fragmented ValueBlock"],
                     }

        if str(obf_params) not in result.keys():
            result[str(obf_params)] = {}

        if obf_md5 not in result[str(obf_params)].keys():
            result[str(obf_params)][obf_md5] = {"DETON": obf_score}

        if input_md5 not in result[str(obf_params)][obf_md5].keys():
            result[str(obf_params)][obf_md5][input_md5] = calc_score.get_dict()

        if "plain" not in result.keys():
            result["plain"] = {}
        result["plain"]["DETON"] = plain_score
    else:
        if "plain" not in result.keys():
            result["plain"] = {}
        if input_md5 not in result["plain"].keys():
            result["plain"][input_md5] = calc_score.get_dict()

    with open(exp_name, "w") as f:
        f.write(json.dumps(result, indent=4))


def compile_obf(input_path, obfuscator_params, O=0):
    folder = os.path.dirname(input_path)
    obf_folder =  os.path.join(folder, "obfuscated")

    output_path = os.path.join(folder, "obf.out")
    obfuscated_asm = os.path.join(folder, "obf.s")
    asm = os.path.join(folder, "out_no_symbols.s")
    asm_json = os.path.join(folder, "out_no_symbols.json")
    compile_asm_nosymbols(input_path, asm, O=O)
    parse(asm, asm_json)
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        if i > 100:
            exit(-0x61)
        try:
            obfuscate_bench(asm_json, *obfuscator_params)
            os.rename(asm_json + ".s", obfuscated_asm)
            compile_exec(obfuscated_asm, output_path)
            if not test_integrity(os.path.join(folder, "test.out"), output_path):
                obf_success = False
                print("\033[91mFailed output integrity\033[0m", file=sys.stderr)
            else:
                obf_success = True
                str_params = str(obfuscator_params[1]) + "_" + str(obfuscator_params[2]) + "_" + str(obfuscator_params[3]) + "_" + str(obfuscator_params[4])
                os.rename(output_path, os.path.join(obf_folder, str_params + "_" + file_md5(output_path)))
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    return


def file_md5(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        md5_hash.update(f.read())

    return md5_hash.hexdigest()


def test_integrity(plain, obf):
    process1 = subprocess.Popen([plain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out1, err1 = process1.communicate()
    process2 = subprocess.Popen([obf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out2, err2 = process2.communicate()

    return out1 == out2 and err1 == err2


def run_dump(exec_params, ignore_cache=True, exclude=None, timeout=90000):
    print("# EXECUTE DUMP #")
    start_time = time.time()
    plain_execution_dump = edg.edg(exec_params[0], exec_params, ignore_cache=ignore_cache, exclude=exclude, timeout=timeout)
    print("--- %s seconds ---" % (time.time() - start_time))
    return plain_execution_dump


def run_trace(plain_execution_dump, symbols_elf, trace_no_symbols=True):
    print("# EXECUTE TRACE #\n")
    start_time = time.time()
    local_vars, global_vars, arrays = offset_finder.offset_finder(symbols_elf)
    tracer = Tracer(local_vars, global_vars, plain_execution_dump, arrays=arrays)
    tracer.start_trace(trace_no_symbols=trace_no_symbols)
    print("--- %s seconds ---" % (time.time() - start_time))
    return tracer


def run_score(tracer):
    print("# CALCULATE SCORE #")
    start_time = time.time()
    metrics = Metrics(tracer)
    metrics.metric_score()
    print("--- %s seconds ---" % (time.time() - start_time))
    return metrics


def execute_plain(source_file: str, compile_method=compile_program, args=[], exclude=None):
    sys.setrecursionlimit(10 ** 4)

    asm = "out_no_symbols.s"
    folder = os.path.dirname(source_file)
    executable_elf = os.path.join(folder, "test.out")

    exec_params = [executable_elf] + args

    plain_execution_dump = run_dump(exec_params, exclude=exclude)
    tracer = run_trace(plain_execution_dump, executable_elf, trace_no_symbols=False)
    return tracer


def execute_obfuscated_bench(obf_exec_params, symbols_elf="../test.out"):
    sys.setrecursionlimit(10 ** 4)

    folder = os.path.dirname(obf_exec_params[0])

    obf_execution_dump = run_dump(obf_exec_params, ignore_cache=True, exclude=None, timeout=90000)

    trace = run_trace(obf_execution_dump, os.path.join(folder, symbols_elf), trace_no_symbols=False)

    score = {}
    with open(os.path.join(folder, "../out_no_symbols.json_metrics.txt"), "r") as f:
        for line in f:
            key_line, value = line.split(":")
            score[key_line] = json.loads(value.split("->")[0])

    return trace, score