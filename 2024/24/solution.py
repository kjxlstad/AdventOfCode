import re
from typing import Iterator

GATE_PATTERN = r"(\w+) ([A-Z]+) (\w+) -> (\w+)"


def simulate_circuit(
    state: dict[str, int], gates: dict[str, tuple[str, str, str]]
) -> Iterator[int]:
    def evaluate(wire: str) -> int:
        if wire in state:
            return state[wire]

        wire1, operator, wire2 = gates[wire]
        match operator:
            case "AND":
                return evaluate(wire1) & evaluate(wire2)
            case "XOR":
                return evaluate(wire1) ^ evaluate(wire2)
            case "OR":
                return evaluate(wire1) | evaluate(wire2)

    return (evaluate(wire) for wire in sorted(gates) if wire.startswith("z"))


if __name__ == "__main__":
    state, gates = open("data.in").read().split("\n\n")

    state = {w: int(s) for w, s in (line.split(": ") for line in state.splitlines())}
    gates = {out: in_ for *in_, out in re.findall(GATE_PATTERN, gates)}

    # Part 1
    print(sum(v << i for i, v in enumerate(simulate_circuit(state, gates))))
