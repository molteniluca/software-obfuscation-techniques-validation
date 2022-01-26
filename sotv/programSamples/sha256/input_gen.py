import os
import hashlib


def build_inputs():
    lengths = []

    for i in range(5):
        lengths.append(10)

    lengths.append(100)
    lengths.append(200)
    lengths.append(300)
    lengths.append(400)
    lengths.append(500)
    lengths.append(1000)

    for elem in lengths:
        data = os.urandom(elem)
        open("./inputs/"+hashlib.md5(data.replace(b"\x00", b"\x01")).hexdigest(), "wb").write(data)


if __name__ == "__main__":
    build_inputs()
