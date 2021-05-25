import json
import subprocess
from os import system

if __name__ == "__main__":
    system("qemu-riscv64-static -g 1234 ./a.out &")  # Starts qemu session in background
    subprocess.run(["gdb-multiarch", "-command=EDG_script.py"])


def EDG():
    system("qemu-riscv64-static -g 1234 ./a.out &")  # Starts qemu session in background
    subprocess.run(["gdb-multiarch", "-command=EDG_script.py"])
    return json.loads("dump.json")
