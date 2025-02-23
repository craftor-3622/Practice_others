import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vector(value * self.x, value * self.y)

    def multiply(self, coefficient: float):
        self.x *= coefficient
        self.y *= coefficient

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def unit_vector(self):
        x_n, y_n = self.x / self.magnitude(), self.y / self.magnitude()
        return Vector(x_n, y_n)


def dot_product(self, other) -> int:
    return self.x * other.x + self.y * other.y


def collision(a_pos: Vector, a_speed: Vector, b_pos: Vector):
    normal_vec = Vector.unit_vector(b_pos - a_pos)
    tangent_vec = Vector(-normal_vec.y, normal_vec.x)
    
    scalar_vn = dot_product(a_speed, normal_vec)
    vector_vn = normal_vec * scalar_vn
    scalar_vt = dot_product(a_speed, tangent_vec)
    vector_vt = tangent_vec * scalar_vt


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
Hit_n = Hit.unit_vector()
print(Hit.x, Hit.y)
print(Hit_n.x, Hit_n.y)
direction = Hit - my_ball
distance = direction.magnitude()

theta = math.degrees(math.atan(direction.y/direction.x))
print(direction.x, direction.y)
print(distance)
print(theta)