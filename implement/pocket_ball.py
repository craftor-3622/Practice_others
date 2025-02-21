import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def multiply(self, coefficient: float):
        self.x *= coefficient
        self.y *= coefficient

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def normal_vector(self):
        x_n, y_n = self.x / self.magnitude(), self.y / self.magnitude()
        return Vector(x_n, y_n)


def collision(a_ball: Vector, b_ball: Vector):
    pass


def bound_wall():
    pass


diameter = 5.73
board_x, board_y = 254, 127

hole = Vector(254, 127)
ball = Vector(240, 120)
my_ball = Vector(100, 100)

Hole_angle = math.atan((hole.y - ball.y) / (hole.x - ball.x))

Hit = Vector(ball.x - diameter*math.cos(Hole_angle), ball.y - diameter*math.sin(Hole_angle))
Cushion = Vector(ball.x - diameter*math.cos(Hole_angle), ball.y + diameter*math.sin(Hole_angle))
Hit_n = Hit.normal_vector()
print(Hit.x, Hit.y)
print(Hit_n.x, Hit_n.y)
direction = Hit - my_ball
distance = direction.magnitude()

theta = math.degrees(math.atan(direction.y/direction.x))
print(direction.x, direction.y)
print(distance)
print(theta)