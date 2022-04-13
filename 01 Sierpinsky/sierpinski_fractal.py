from dataclasses import dataclass
import matplotlib.pyplot as plt
import random


@dataclass
class Point:
    x: float
    y: float


def create_middle_point(point_a, point_b):
    new_x = (point_a.x + point_b.x) / 2.0
    new_y = (point_a.y + point_b.y) / 2.0

    return Point(new_x, new_y)


point_one = Point(1, 1)
point_two = Point(22, 1)
point_three = Point(11, 22)

plt.scatter(point_one.x, point_one.y, c="#000")
plt.scatter(point_two.x, point_two.y, c="#000")
plt.scatter(point_three.x, point_three.y, c="#000")

initial_points = [point_one, point_two, point_three]
starting_point = create_middle_point(point_one, point_two)
# choose a random point
random_pivot_point = random.choice(initial_points)
new_point = create_middle_point(starting_point, random_pivot_point)
# draw the point
plt.scatter(new_point.x, new_point.y, s=1)

for i in range(7000):
    random_pivot_point = random.choice(initial_points)
    new_point = create_middle_point(starting_point, random_pivot_point)
    plt.scatter(new_point.x, new_point.y, s=1)
    starting_point = new_point
