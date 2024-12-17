from typing import Iterator

from z3 import BitVec, BitVecRef, Solver, sat

BitVecRef.__floordiv__ = BitVecRef.__truediv__
BitVecRef.__rfloordiv__ = BitVecRef.__rtruediv__

INSTRUCTIONS = "adv bxl bst jnz bxc out bdv cdv".split()


# assumes last three instructions are adv, out, jnz
# out, adv, jnz won't work with z3 because of yield order
def execute(
    registers: dict[str, int | BitVecRef], program: list[int], loop: bool = False
) -> Iterator[int]:
    ip = 0

    while ip < len(program):
        opcode, operand = program[ip : ip + 2]
        combo_reg = dict(zip([4, 5, 6], registers.values()))
        combo_operand = combo_reg.get(operand, operand)

        # fmt: off
        match INSTRUCTIONS[opcode]:
            case "adv": registers["A"] = registers["A"] // (1 << combo_operand)
            case "bdv": registers["B"] = registers["A"] // (1 << combo_operand)
            case "cdv": registers["C"] = registers["A"] // (1 << combo_operand)
            case "bst": registers["B"] = combo_operand % 8
            case "bxc": registers["B"] ^= registers["C"]
            case "bxl": registers["B"] ^= operand

            case "out": yield combo_operand % 8
            case "jnz" if loop or registers["A"]: ip = operand - 2
        # fmt: on
        ip += 2


def quinic_registers(program: list[int]) -> Iterator[int]:
    solver = Solver()
    a_init = BitVec("a_init", 49)  # 48 + sign bit
    registers = {"A": a_init, "B": 0, "C": 0}

    for instruction, output in zip(program, execute(registers, program, loop=True)):
        solver.add(instruction == output)

    solver.add(registers["A"] == 0)

    while solver.check() == sat:
        model = solver.model().eval(a_init)
        yield {"A": model.as_long(), "B": 0, "C": 0}
        solver.add(a_init < model)


if __name__ == "__main__":
    registers, program = open("data.in").read().split("\n\n")
    registers = {reg: int(line[12:]) for reg, line in zip("ABC", registers.split("\n"))}
    program = [int(opcode) for opcode in program[9:].split(",")]

    # Part 1
    print(*execute(registers, program), sep=",")

    # Part 2
    print(min(register["A"] for register in quinic_registers(program)))
