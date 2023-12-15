from functools import reduce


def ascii_hash(string):
    return reduce(lambda acc, new: (acc + ord(new)) * 17 % 256, string, 0)


def focusing_power(boxes):
    return sum(
        focal_length * box_num * slot_num
        for box_num, box in enumerate(boxes, start=1)
        for slot_num, focal_length in enumerate(box.values(), start=1)
    )


def place_lenses(instructions):
    boxes = [{} for _ in range(256)]
    for instruction in instructions:
        match list(instruction):
            case [*label, "=", focal_length]:
                slot = boxes[ascii_hash(label)]
                slot["".join(label)] = int(focal_length)
            case [*label, "-"]:
                slot = boxes[ascii_hash(label)]
                label = "".join(label)
                if label in slot:
                    del slot["".join(label)]
    return boxes


if __name__ == "__main__":
    with open("data.in", "r") as f:
        strings = f.read().split(",")

    # Part 1
    print(sum(map(ascii_hash, strings)))

    # Part 2
    print(focusing_power(place_lenses(strings)))
