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
