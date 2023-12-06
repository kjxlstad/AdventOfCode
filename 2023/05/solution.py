import re
from functools import reduce
from collections import namedtuple

Interval = namedtuple("Interval", ["start", "length"])


def parse_nums(line):
    return [int(x) for x in re.findall(r"\d+", line)]


def parse_almanac(almanac):
    seed_line, *rule_sections = almanac.read().split("\n\n")

    seeds = parse_nums(seed_line)
    rules = [
        [parse_nums(line) for line in section.split("\n")[1:]]
        for section in rule_sections
    ]

    return seeds, rules


def map_(num, mappings):
    for dst, src, len in mappings:
        offset = num - src
        if offset in range(len):
            return [dst + offset]

    return [num]


def map_interval(interval, mappings):
    if interval.length == 0:
        return []

    for dst, src, len in mappings:
        offset = interval.start - src
        if offset in range(len):
            cut = min(len - offset, interval.length)
            
            return [Interval(dst + offset, cut)] + map_interval(
                Interval(interval.start + cut, interval.length - cut), mappings
            )

    return [interval]


def propogate(values, mappings, map_func):
    def prop(values, mappings):
        if not values:
            return []

        value, *values = values
        return map_func(value, mappings) + prop(values, mappings)

    return reduce(prop, mappings, values)


if __name__ == "__main__":
    with open("data.in") as almanac:
        seeds, rules = parse_almanac(almanac)

    # Part 1
    locations = propogate(seeds, rules, map_)
    print(min(locations))

    # Part 2
    seed_intervals = [
        Interval(start, length)
        for start, length in zip(seeds[0::2], seeds[1::2])
    ]

    location_intervals = propogate(seed_intervals, rules, map_interval)
    print(min(interval.start for interval in location_intervals))
