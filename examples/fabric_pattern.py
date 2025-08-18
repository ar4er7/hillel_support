from math import cos, sin


class Point:
    def __init__(self, x, y):  # constructor to initialize x and y coordinates
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    @staticmethod  # fabric method to create a new Point from Cartesian coordinates
    def new_cartesian_point(x, y):
        return Point(x, y)

    @staticmethod  # fabric method to create a new Point from polar coordinates
    def new_polar_point(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))


if __name__ == "__main__":
    p = Point(3, 4)  # creating a point as an instance of Point
    p2 = Point.new_polar_point(
        5, 6
    )  # creating a point as fabric method from polar coordinates

    print(p)
    print(p2)
