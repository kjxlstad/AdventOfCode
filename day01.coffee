fs = require 'fs'

data = fs.readFileSync 'data/day01.in', 'utf8'
sweeps = (parseInt sweep for sweep in data.split '\n')

# Part 1
chain = (iterable, n) ->
    (iterable[i...i + n] for i in [0 ... iterable.length - n + 1])

countIncreasing = (iterable) ->
    chain iterable, 2
        .filter (pair) -> pair[0] < pair[1]
        .length

console.log countIncreasing sweeps

# Part 2
triplets = chain sweeps, 3
    .map (triplet) ->
        triplet.reduce (a, b) -> a + b

console.log countIncreasing triplets