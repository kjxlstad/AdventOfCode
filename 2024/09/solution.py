from dataclasses import dataclass
from itertools import accumulate
from typing import Iterator


@dataclass
class Chunk:
    id: str
    size: int
    pos: int

    def occupy(self, file: "Chunk") -> "Chunk":
        self.size -= file.size
        self.pos += file.size


def expand_dense(dense_format: str) -> list[int | None]:
    return [
        None if i % 2 else i // 2
        for i, size in enumerate(map(int, dense_format))
        for _ in range(size)
    ]


def compact(disk: list[int | None]) -> list[int | None]:
    left, right = 0, len(disk) - 1

    while left < right:
        if disk[left] is not None:
            left += 1
        elif disk[right] is None:
            right -= 1
        else:
            disk[left], disk[right] = disk[right], disk[left]

    return disk


def create_blocks(dense_format: str) -> tuple[list[Chunk], list[Chunk]]:
    sizes = list(map(int, dense_format))
    positions = list(accumulate(sizes, initial=0))[:-1]

    files = [Chunk(i // 2, sizes[i], positions[i]) for i in range(0, len(sizes), 2)]
    spaces = [Chunk(".", sizes[i], positions[i]) for i in range(1, len(sizes), 2)]

    return files, spaces


def find_space(spaces: list[Chunk], file: Chunk) -> Chunk | None:
    for empty in spaces:
        if empty.size >= file.size and empty.pos < file.pos:
            return empty
    return None


def compressed_files(files: list[Chunk], spaces: list[Chunk]) -> Iterator[Chunk]:
    for file in reversed(files):
        if (empty_space := find_space(spaces, file)) is not None:
            yield Chunk(file.id, file.size, empty_space.pos)
            empty_space.occupy(file)
        else:
            yield file


if __name__ == "__main__":
    dense_format = open("data.in").read()

    # Part 1
    fragmented = compact(expand_dense(dense_format))
    print(sum(i * id for i, id in enumerate(fragmented) if id is not None))

    # Part 2
    compressed = compressed_files(*create_blocks(dense_format))
    print(sum((f.pos + i) * f.id for f in compressed for i in range(f.size)))
