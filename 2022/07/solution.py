from collections import defaultdict

def update_tree(cmd, tree, path):
    match cmd.split(" "):
        case ["$", "cd", ".."]: path.pop()
        case ["$", "cd", p]: path.append(p)
        case ["$", "ls"] | ["dir", _]: pass
        case [size, _]: update_size(tree, path, int(size))


def update_size(tree, path, size):
    for parent in [path[: i + 1] for i in range(len(path))]:
        tree[tuple(parent)] += size


def parse_file_tree(cmds):
    tree = defaultdict(int)
    path = []

    for cmd in cmds:
        update_tree(cmd, tree, path)

    return tree


if __name__ == "__main__":
    with open("data.in", "r") as f:
        file_tree = parse_file_tree(f.read().split("\n"))

    # Part 1
    print(sum(s for s in file_tree.values() if s <= 100_000))

    # part 2
    free_space = 70_000_000 - file_tree[("/",)]
    print(min(s for s in file_tree.values() if s + free_space >= 30_000_000))
