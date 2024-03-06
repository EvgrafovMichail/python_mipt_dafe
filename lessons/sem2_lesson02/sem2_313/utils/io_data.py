import struct

from typing import Any


def read_floats_from_bytes(
    bytes_amount: int,
    path_to_file: str,
) -> list[float]:
    with open(path_to_file, "rb") as file:
        buffer = file.read()

    floats = struct.unpack(f"{bytes_amount}f", buffer)
    return floats


def print_matrix(matrix: list[Any]) -> None:
    for row in matrix:
        print(row)

    print("")
