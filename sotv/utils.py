import os
from os import system

from sotv.exceptions.SubProcessFailedException import SubProcessFailedException

# obfuscator_path = "./Obfuscator/RISCV-Obfuscator/"
obfuscator_path = "/home/pii/pii/RISCV-Obfuscator/"
obfuscator2_path = "/home/pii/PycharmProjects/DETON/"

def compile_asm(input_path: str, output_path: str):
    if system(
            "riscv64-linux-gnu-gcc -g -S --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-strict-align -mpreferred-stack-boundary=4 -static -fno-stack-protector "
            + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_exec(input_path: str, output_path: str, O=0):
    if system("riscv64-linux-gnu-gcc -g --no-PIC -O" + str(O)
              + " -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -mno-strict-align -mpreferred-stack-boundary=4 -fno-stack-protector "
              + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_asm_nosymbols(input_path: str, output_path: str, O=0):
    if system("riscv64-linux-gnu-gcc -S --no-PIC -O" + str(O)
              + " -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-strict-align -mpreferred-stack-boundary=4 -static -fno-stack-protector "
              + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def obfuscate(input_path: str, output_path: str, entry_point: str, rep_value: int, heat_value: int):
    if system("PYTHONPATH=\"" + obfuscator_path + "\" /usr/bin/python3.8 " + obfuscator_path + "/rvob/main.py "
              + input_path + " " + entry_point + " " + str(rep_value) + " " + str(heat_value) + " " +
              output_path) != 0:
        raise SubProcessFailedException


def obfuscate_bench(input_path: str, entry_point: str, rep_scrambling: int, rep_obfuscate: int, rep_garbage: int, heat_value: int):
    '''if system("PYTHONPATH=\"" + obfuscator_path + "\" /usr/bin/python3.8 " + obfuscator_path + "/rvob/benchmark.py "
              + os.path.abspath(input_path) + " " + entry_point + " " + str(rep_scrambling) + " " + str(rep_obfuscate) + " "
              + str(rep_garbage) + " " + str(heat_value)) != 0:
        raise SubProcessFailedException
    obfuscate(input_path, os.path.join(os.path.dirname(input_path), "out_no_symbols.json.s"), entry_point, rep_scrambling, rep_obfuscate)'''
    obfuscate_bench_2(input_path, input_path+".s", entry_point, rep_scrambling, rep_obfuscate, 1, rep_garbage, heat_value)


def obfuscate_bench_2(input_path: str, output_path:str, entry_point: str, rep_scrambling: int, rep_obfuscate: int, size_block:int, rep_garbage: int, heat_value: int):
    if system("PYTHONPATH=\"" + obfuscator2_path + "\" /usr/bin/python3.8 " + obfuscator2_path + "/rvob/deton.py "
              + os.path.abspath(input_path) + " " + str(rep_scrambling) + " " +
              str(rep_obfuscate) + " " + str(rep_garbage) + " " + str(size_block) + " " + str(heat_value) + " " + os.path.abspath(output_path)
              + " -m" + " -e " + entry_point) != 0:
        raise SubProcessFailedException


def parse(input_path: str, output_path: str):
    return system("./EDG/parser " + input_path + " " + output_path) == 0


if __name__ == "__main__":
    compile_exec("programSamples/test.c", "a.out")

