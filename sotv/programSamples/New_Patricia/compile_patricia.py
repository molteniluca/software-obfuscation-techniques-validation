import os.path
import subprocess
import sys
from os import system

from sotv.EDG import edg
from sotv.EDG.exceptions.DumpFailedException import DumpFailedException
from sotv.exceptions.SubProcessFailedException import SubProcessFailedException
from sotv.utils import parse, obfuscate_bench, compile_exec


def compile_patricia(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector -o "+ path +"/patricia " + path + "/*.c") != 0:
        raise SubProcessFailedException


def compile_patricia_nosymbols(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0  -static -fno-stack-protector -S " + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_obf(input_path: str, output_path: str):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector -o " + output_path + " " + os.path.dirname(input_path) + "/patricia_test.c "+ os.path.dirname(input_path) + "/obf.s") != 0:
        raise SubProcessFailedException


def compile_program_patricia(source_file, executable_elf):
    folder = "./programSamples/New_Patricia/"

    compile_patricia(source_file, folder + executable_elf, folder)
    os.rename(os.path.join(folder, "patricia"), os.path.join(folder, "test.out"))


def test_integrity(plain, obf, param):
    process1 = subprocess.Popen([plain, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out1, err1 = process1.communicate()
    process2 = subprocess.Popen([obf, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out2, err2 = process2.communicate()

    return out1 == out2 and err1 == err2


def compile_obf_patricia(input_path, output_path, obfuscator_params, obf_exec_params, O=0):
    folder = os.path.dirname(input_path)
    obfuscated_asm = os.path.join(folder, "obf.s")
    asm = os.path.join(folder, "out_no_symbols.s")
    asm_json = os.path.join(folder, "out_no_symbols.json")
    compile_patricia_nosymbols(os.path.join(folder, "patricia.c"), asm, folder)
    parse(asm, asm_json)
    obf_success = False
    i = 0

    while not obf_success:
        i += 1
        try:
            obfuscate_bench(asm_json, *obfuscator_params)
            os.rename(asm_json+".s", obfuscated_asm)
            compile_obf(obfuscated_asm, output_path)
            if not test_integrity(os.path.join(folder, "test.out"), output_path, os.path.join(folder, "small.udp")):
                obf_success = False
                print("\033[91mFailed output integrity\033[0m", file=sys.stderr)
            else:
                try:
                    obf_execution_dump = edg.edg(os.path.basename(input_path) + "_last_obf", obf_exec_params, ignore_cache=True)
                    obf_success = True
                except DumpFailedException as e:
                    obf_success = False
        except SubProcessFailedException as e:
            print("Failed obfuscation attempt:" + str(i))
            obf_success = False

    return obf_execution_dump