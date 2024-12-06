def processed_before_marker(datastream, markersize):
    chunks = (datastream[i : i + markersize] for i, _ in enumerate(datastream))
    processed = next(i for i, c in enumerate(chunks) if len(set(c)) == markersize)
    return processed + markersize


if __name__ == "__main__":
    with open("data.in", "r") as f:
        datastream = f.read()

    # Part 1
    print(processed_before_marker(datastream, 4))

    # Part 2
    print(processed_before_marker(datastream, 14))
