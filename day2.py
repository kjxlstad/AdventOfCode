data = [line.split(" ") for line in open("data/day2.in", "r").readlines()]
cmds = [(cmd, int(mag)) for cmd, mag in data]

# Part 1 & 2
pos, depth, aim = 0, 0, 0
for cmd, mag in cmds:
    if cmd == "forward":
        pos += mag
        depth += mag * aim
    elif cmd == "down":
        aim += mag
    else:
        aim -= mag

print(pos * aim)
print(pos * depth)
