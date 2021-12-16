from operator import gt, lt, eq
from math import prod
from itertools import takewhile, repeat

unpack = lambda func: lambda v: int(func(*v))

OPERATORS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: unpack(gt),
    6: unpack(lt),
    7: unpack(eq),
}


def hex_to_bin(hex):
    return bin(int(hex, 16))[2:].zfill(4)


class Stream:
    def __init__(self, bits):
        self.bits = bits
        self.i = 0
        self.version_total = 0

    def consume(self, n):
        consumed, rest = self.bits[:n], self.bits[n:]
        self.bits = rest
        self.i += n
        return consumed


def decode_literal(stream):
    def decode(bits):
        literal = stream.consume(5)

        if literal[0] == "1":
            return literal[1:5] + decode(stream)

        return literal[1:5]

    return int(decode(stream), 2)


def decode_operator(stream, operator):
    prefix = stream.consume(1)

    if prefix == "1":
        sub_packets = int(stream.consume(11), 2)
        v = [decode_packet(stream) for _ in range(sub_packets)]

    elif prefix == "0":
        sub_packet_length = int(stream.consume(15), 2)

        def read(end):
            return [decode_packet(stream)] + read(end) if stream.i < end else []

        v = read(stream.i + sub_packet_length)

    return operator(v)


def decode_packet(stream):
    version = stream.consume(3)
    stream.version_total += int(version, 2)

    type_id = int(stream.consume(3), 2)

    if type_id != 4:
        return decode_operator(stream, OPERATORS[type_id])

    return decode_literal(stream)


if __name__ == "__main__":
    bits = hex_to_bin(open("data.in", "r").read().strip())
    stream = Stream(bits)

    result = decode_packet(stream)

    # Part 1
    print(stream.version_total)

    # Part 2
    print(result)
