import re

MUL_PATTERN = r"mul\((\d+),(\d+)\)"
DOMUL_PATTERN = rf"(do)\(\)|(don't)\(\)|{MUL_PATTERN}"


def enabled_operands():
    enabled = True

    for match in re.finditer(DOMUL_PATTERN, memory):
        if match.group(1):
            enabled = True
        elif match.group(2):
            enabled = False
        elif enabled:
            yield int(match.group(3)), int(match.group(4))


if __name__ == "__main__":
    memory = open("data.in").read()

    # Part 1
    print(sum(int(a) * int(b) for a, b in re.findall(MUL_PATTERN, memory)))

    # Part 2
    print(sum(a * b for a, b in enabled_operands()))
