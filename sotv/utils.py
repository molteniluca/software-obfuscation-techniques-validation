import os
from os import system


def compile_asm(input_path: str, output_path: str):
    system("riscv64-linux-gnu-gcc -g -S --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
           + input_path + " -o " + output_path)


def compile_exec(input_path: str, output_path: str):
    system("riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
           + input_path + " -o " + output_path)


def compile_asm_nosymbols(input_path: str, output_path: str):
    system("riscv64-linux-gnu-gcc -S --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
           + input_path + " -o " + output_path)


def obfuscate(input_path: str, output_path: str, rep_value: int, heat_value: int):
    system("PYTHONPATH=\"/home/pii/pii/RISCV-Obfuscator/\" /usr/bin/python3.8 /home/pii/pii/RISCV-Obfuscator/rvob/main.py "
           + input_path + " main " + str(rep_value) + " " + str(heat_value) + " " + output_path)


def parse(input_path: str, output_path: str):
    system("./EDG/parser " + input_path + " " + output_path)


if __name__ == "__main__":
    compile_exec("programSamples/test.c", "a.out")
