from operator import gt, lt, eq
from math import prod


def unpack(func):
    return lambda v: int(func(*v))


def hex_to_bin(hex):
    return bin(int(hex, 16))[2:].zfill(4)


OPERATORS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: unpack(gt),
    6: unpack(lt),
    7: unpack(eq),
}


class Stream:
    def __init__(self, bits):
        self.bits = bits
        self.i = 0
        self.version_total = 0

    def consume(self, n):
        consumed, self.bits = self.bits[:n], self.bits[n:]
        self.i += n
        return consumed


def decode_literal(stream):
    def decode():
        return (
            stream.consume(4) + decode() if int(stream.consume(1)) else stream.consume(4)
        )

    return int(decode(), 2)


def decode_operator(stream, operator):
    prefix = stream.consume(1)

    if int(prefix):
        num_sub_packets = int(stream.consume(11), 2)
        sub_packets = [decode_packet(stream) for _ in range(num_sub_packets)]
    else:
        sub_packet_length = int(stream.consume(15), 2)

        def read(end):
            return [decode_packet(stream)] + read(end) if stream.i < end else []

        sub_packets = read(stream.i + sub_packet_length)

    return operator(sub_packets)


def decode_packet(stream):
    stream.version_total += int(stream.consume(3), 2)
    type_id = int(stream.consume(3), 2)

    if type_id == 4:
        return decode_literal(stream)

    return decode_operator(stream, OPERATORS[type_id])


if __name__ == "__main__":
    bits = hex_to_bin(open("data.in", "r").read().strip())
    stream = Stream(bits)

    result = decode_packet(stream)

    # Part 1
    print(stream.version_total)

    # Part 2
    print(result)
