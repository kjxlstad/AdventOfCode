from itertools import tee


def nth_wise(iterable, n):
    iterators = tee(iterable, n)
    for i, iterator in enumerate(iterators):
        for _ in range(i):
            next(iterator)
    yield from zip(*iterators)


def processed_before_marker(datastream, markersize):
    chunks = nth_wise(datastream, markersize)
    processed = next(i for i, c in enumerate(chunks) if len(set(c)) == len(c))
    return processed + markersize


if __name__ == "__main__":
    with open("data.in", "r") as f:
        datastream = f.read()

    # Part 1
    print(processed_before_marker(datastream, 4))

    # Part 2
    print(processed_before_marker(datastream, 14))
