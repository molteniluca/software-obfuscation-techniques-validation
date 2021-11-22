from os import system

from sotv.exceptions.SubProcessFailedException import SubProcessFailedException

obfuscator_path = "./Obfuscator/RISCV-Obfuscator/"


def compile_asm(input_path: str, output_path: str):
    if system(
            "riscv64-linux-gnu-gcc -g -S --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
            + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_lib_patricia():
    path = "./programSamples/New_Patricia/"
    system("riscv64-linux-gnu-gcc -g -c " + path + "patricia.c -o" + path+"patricia.o")
    system("riscv64-linux-gnu-ar -r " + path + "libpatricia.a " + path + "patricia.o ")
    system("riscv64-linux-gnu-ranlib " + path + "libpatricia.a")


def compile_patricia(input_path: str, output_path: str, path):
    system("pwd")
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector"
            + " -I " + path + " -L " + path + " " + input_path + " -o " + output_path + " -lpatricia") != 0:
        raise SubProcessFailedException


def compile_patricia_nosymbols(input_path: str, output_path: str, path):
    system("pwd")
    if system(
            "riscv64-linux-gnu-gcc --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector"
            + " -I " + path + " -L " + path + " " + input_path + " -o " + output_path + " -lpatricia") != 0:
        raise SubProcessFailedException


def compile_exec(input_path: str, output_path: str):
    if system("riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
              + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def compile_asm_nosymbols(input_path: str, output_path: str):
    if system("riscv64-linux-gnu-gcc -S --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
              + input_path + " -o " + output_path) != 0:
        raise SubProcessFailedException


def obfuscate(input_path: str, output_path: str, entry_point: str, rep_value: int, heat_value: int):
    if system("PYTHONPATH=\"" + obfuscator_path + "\" /usr/bin/python3.8 " + obfuscator_path + "/rvob/main.py "
              + input_path + " " + entry_point + " " + str(rep_value) + " " + str(heat_value) + " " +
              output_path) != 0:
        raise SubProcessFailedException


def parse(input_path: str, output_path: str):
    return system("./EDG/parser " + input_path + " " + output_path) == 0


if __name__ == "__main__":
    compile_exec("programSamples/test.c", "a.out")
