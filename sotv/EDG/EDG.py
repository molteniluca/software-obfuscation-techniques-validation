import json
import subprocess

if __name__ == "__main__":
    # Starts qemu session in background
    subprocess.Popen(["qemu-riscv64-static", "-g", "1234", "./a.out"])
    subprocess.run(["gdb-multiarch", "-command=EDG_script.py", "-batch-silent"])


def edg(executable_params: list) -> list:
    # Starts qemu session in background
    subprocess.Popen(["qemu-riscv64-static", "-g", "1234"] + executable_params)
    subprocess.run(["gdb-multiarch", "-command=./EDG/EDG_script.py", "-batch-silent"])

    return json.loads(open("dump.json", "r").read())
