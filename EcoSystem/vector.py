import math

MAP_SIZE = 50


class Vector:
    def __init__(self, X: int, Y: int) -> None:
        self.X = X
        self.Y = Y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __add__(self, otherPos):
        return Vector(self.X + otherPos.X, self.Y + otherPos.Y)

    def __sub__(self, otherPos):
        return Vector(self.X - otherPos.X, self.Y - otherPos.Y)

    def __mul__(self, num):
        return Vector(num * self.X, num * self.Y)

    def __str__(self) -> str:
        return f"Vector: ({str(self.X)}, {str(self.Y)})"

    def distance2(self, otherPos) -> int:
        return (self.X - otherPos.X) ** 2 + (self.Y - otherPos.Y) ** 2

    def distance(self, otherPos):
        return ((self.X - otherPos.X) ** 2 + (self.Y - otherPos.Y) ** 2) ** 0.5

    def inRange(self, otherPos, range):
        # return self.distance2(otherPos) <= range ** 2
        return abs(self.X - otherPos.X) <= range and abs(self.Y - otherPos.Y) <= range



    # 计算传入的另一坐标相对于本坐标的方向，范围 (-PI, PI]，单位是弧度而非角度。
    def direction(self, otherPos):
        x = otherPos.X - self.X
        y = otherPos.Y - self.Y
        # 修改+0,0001防止float division by zero报错
        L = (x**2 + y**2) ** 0.5 + 0.0001
        return math.acos(x / L) if y >= 0 else -1 * math.acos(x / L)

    # direction 是方向，单位弧度，范围 (-PI, PI]
    # 返回下一步要走的坐标
    moveIncrement = [
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
    ]

    radians22_5 = 0.39269908169872414
    radians45 = 0.7853981633974483
    radians180 = 3.141592653589793
    radians202_5 = 3.5342917352885173
    radians360 = 6.283185307179586

    def nextPos(self, direction, speed, reverse=False):
        # if type(directionOrPos) == type(.1):
        # direction = directionOrPos

        # 加 0.5 是为了四舍五入
        dX = int(speed * math.cos(direction) + 0.5)
        dY = int(speed * math.sin(direction) + 0.5)

        return (
            Vector(self.X + dX, self.Y + dY)
            if reverse == False
            else Vector(self.X - dX, self.Y - dY)
        )

        # return (
        #     self
        #     + Vector(
        #         *Vector.moveIncrement[
        #             ((direction + Vector.radians202_5) % Vector.radians360)
        #             // Vector.radians45
        #         ]
        #     )
        #     if reverse == False
        #     else self
        #     + Vector(
        #         *Vector.moveIncrement[
        #             (
        #                 ((direction + Vector.radians202_5) % Vector.radians360)
        #                 // Vector.radians45
        #                 + 4
        #             )
        #             % 8
        #         ]
        #     )
        # )

        # elif type(directionOrPos) == type(self):
        #     x = directionOrPos.X - self.X
        #     y = directionOrPos.Y - self.Y
        #     L = (x**2 + y**2)**0.5
        #     direction =  math.acos(y/L) if y >= 0 else -1*math.acos(y/L)
        #     return self + Vector(
        #         * Vector.moveIncrement[((direction + Vector.radians202_5) % Vector.radians360) // Vector.radians45]
        #     ) if reverse == False else self + Vector(
        #         * Vector.moveIncrement[(((direction + Vector.radians202_5) % Vector.radians360) // Vector.radians45 + 4) % 8]
        #     )

    def weightedSum(weightLst, directionLst, reverse=False):
        if len(weightLst) != len(directionLst):
            raise ValueError()
        x, y = 0, 0
        for i, weight in enumerate(weightLst):
            x += weight * math.cos(directionLst[i])
            y += weight * math.sin(directionLst[i])
        L = (x**2 + y**2) ** 0.5 + 0.001  # 防止生物重叠时距离为零
        sumDirection = math.acos(x / L) if y >= 0 else -1 * math.acos(x / L)
        if reverse == False:
            return L, sumDirection
        elif reverse == True:
            if sumDirection > 0:
                return L, sumDirection - Vector.radians180
            elif sumDirection <= 0:
                return L, sumDirection + Vector.radians180
