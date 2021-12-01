from os import system

from sotv.exceptions.SubProcessFailedException import SubProcessFailedException


def compile_lib_patricia():
    path = "./programSamples/New_Patricia/"
    system("riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-fdiv -mno-strict-align -static -fno-stack-protector -c " + path + "patricia.c -o" + path+"patricia.o")
    system("riscv64-linux-gnu-ar -r " + path + "libpatricia.a " + path + "patricia.o ")
    system("riscv64-linux-gnu-ranlib " + path + "libpatricia.a")


def compile_patricia(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector"
            + " -I " + path + " -L " + path + " " + input_path + " -o " + output_path + " -lpatricia") != 0:
        raise SubProcessFailedException


def compile_patricia_nosymbols(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -mno-fdiv -mno-strict-align -static -fno-stack-protector -S"
            + " -I " + path + " -L " + path + " " + input_path + " -o " + output_path + " -lpatricia") != 0:
        raise SubProcessFailedException


def compile_program_patricia(source_file, executable_elf, asm, folder):
    folder = "./programSamples/New_Patricia/"
    compile_lib_patricia()
    compile_patricia(source_file, folder + executable_elf, folder)
    compile_patricia_nosymbols(source_file, folder + asm, folder)
