from os import system


from sotv.exceptions.SubProcessFailedException import SubProcessFailedException


def compile_fft_symbol(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc -g --no-PIC -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
            + input_path + " -o " + output_path + " -lm ") != 0:
        raise SubProcessFailedException


def compile_fft_nosymbols(input_path: str, output_path: str, path):
    if system(
            "riscv64-linux-gnu-gcc --no-PIC -S -march=rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0 -static -fno-stack-protector "
            + input_path + " -o " + output_path + " -lm ") != 0:
        raise SubProcessFailedException


def compile_program_fft(source_file, executable_elf, asm, folder):
    folder = "./programSamples/New_FFT/"
    compile_fft_symbol(source_file, folder + executable_elf, folder)
    compile_fft_nosymbols(source_file, folder + asm, folder)