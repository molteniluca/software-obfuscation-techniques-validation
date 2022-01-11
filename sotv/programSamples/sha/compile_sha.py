import os.path
import subprocess
import sys
from os import system

from sotv.EDG import edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.utils import parse, obfuscate_bench, compile_exec


def compile_sha(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-strict-align -mpreferred-stack-boundary=4 -static -fno-stack-protector -o "+ path +"/sha " + path + "/sha.c") != 0:
        raise SubProcessFailedException


def compile_sha_nosymbols(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-strict-align -mpreferred-stack-boundary=4  -static -fno-stack-protector -S " + path + "/sha.c -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_obf(input_path: str, output_path: str):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-strict-align -mpreferred-stack-boundary=4 -static -fno-stack-protector -o " + output_path + " " + os.path.dirname(input_path) + "/obf.s") != 0:
        raise SubProcessFailedException


def compile_program_sha(source_file, executable_elf):
    folder = "./programSamples/sha/"

    compile_sha(source_file, folder + executable_elf, folder)
    os.rename(os.path.join(folder, "sha"), os.path.join(folder, "test.out"))


def compile_obf_sha(input_path, output_path, obfuscator_params, obf_exec_params, O=0):
    folder = os.path.dirname(input_path)
    obfuscated_asm = os.path.join(folder, "obf.s")
    asm = os.path.join(folder, "out_no_symbols.s")
    asm_json = os.path.join(folder, "out_no_symbols.json")
    compile_sha_nosymbols(os.path.join(folder, "sha.c"), asm, folder)
    parse(asm, asm_json)
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        try:
            obfuscate_bench(asm_json, *obfuscator_params)
            os.rename(asm_json+".s", obfuscated_asm)
            compile_obf(obfuscated_asm, output_path)
            try:
                obf_execution_dump = edg.edg(os.path.basename(input_path) + "_last_obf",
                                             obf_exec_params, ignore_cache=True, exclude=["main"])
                obf_success = True
            except DumpFailedException as e:
                obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    return obf_execution_dump