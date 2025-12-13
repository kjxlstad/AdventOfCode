from typing import NamedTuple

Shape = NamedTuple("Shape", [("width", int), ("height", int), ("area", int)])
Region = NamedTuple("Region", [("width", int), ("height", int), ("presents", list[int])])

def parse_shape(shape_text: str) -> Shape:
    _, *rows = shape_text.splitlines()
    return Shape(
        max(len(row) for row in rows),
        len(rows),
        sum(row.count("#") for row in rows),
    )

def parse_region(region_text: str) -> Region:
    dimensions, requirements = region_text.split(": ")
    width, height = map(int, dimensions.split("x"))
    presents = [int(count) for count in requirements.split()]
    return Region(width, height, presents)


def fits_presents(region: Region, shapes: list[Shape]) -> bool:
    region_area = region.width * region.height
    presents = [(shapes[i], count) for i, count in enumerate(region.presents)]

    # definitively does not fit if the area is larger than region area
    if sum(shape.area * count for shape, count in presents) > region_area:
        return False

    # definitively fits if region can fit width * height (bounding boxes fit)
    if sum(shape.width * shape.height * count for shape, count in presents) <= region_area:
        return True

    raise NotImplementedError


if __name__ == "__main__":
    with open("data.in", "r") as f:
        *shape_sections, region_section = f.read().split("\n\n")

    shapes = [parse_shape(section) for section in shape_sections]
    regions = [parse_region(line) for line in region_section.splitlines()]

    print(sum(fits_presents(region, shapes) for region in regions))