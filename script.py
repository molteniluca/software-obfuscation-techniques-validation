#system("riscv64-linux-gnu-gcc -g " + c_file + " -nostartfiles")
#system("qemu-riscv64-static -g 1234 ./a.out &")  # Starts qemu session in background