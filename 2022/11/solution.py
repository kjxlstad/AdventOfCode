from operator import add, mul
from functools import reduce
from copy import deepcopy


class Monkey:
    @classmethod
    def from_description(cls, string):
        m = cls()
        m.items = [int(item) for item in string[1][18:].split(", ")]
        m.op, m.val = string[2][23:].split(" ")
        m.divisor = int(string[3][21:])
        m.recipients = int(string[5][30:]), int(string[4][29:])
        m.inspected = 0
        return m

    def inspect(self):
        self.inspected += 1
        w = self.items.pop(0)
        op = {"+": add, "*": mul}[self.op]
        return op(w, w) if self.val == "old" else op(w, int(self.val))

    def find_recipient(self, w):
        return self.recipients[w % self.divisor == 0]


def round(monkeys, worry_reducer):
    for m in monkeys:
        while len(m.items):
            worry_level = worry_reducer(m.inspect())
            recipient = m.find_recipient(worry_level)
            monkeys[recipient].items.append(worry_level)


def monkey_business(monkeys, rounds, worry_reducer):
    for _ in range(rounds): round(monkeys, worry_reducer)
    return mul(*sorted(monkey.inspected for monkey in monkeys)[-2:])


if __name__ == "__main__":
    with open("data.in", "r") as f:
        monkeys = [
            Monkey.from_description(monkey.split("\n"))
            for monkey in f.read().split("\n\n")
        ]

    # Part 1
    print(monkey_business(deepcopy(monkeys), 20, lambda w: w // 3))

    # Part 2
    div = reduce(lambda acc, m: acc * m.divisor, monkeys, 1)
    print(monkey_business(monkeys, 10000, lambda w: w % div))
