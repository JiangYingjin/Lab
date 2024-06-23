# creature —— grass, cattle, tiger
# 属性
# 数量：static?列表长度
# 能量、 移动速度、 当前位置、 出生率(?)
# 函数
# 出生、 死亡、 捕食、 能量消耗、 随机移动(?)
import random
from vector import Vector
import math


class Creature:
    # TypeLst = ["Tiger", "Cow", "Grass"]
    TypeLst = ["老虎", "牛", "草"]

    MAP_SIZE = 50

    INIT_NUM = [0 for _ in range(3)]

    INIT_TIGER_NUM = INIT_NUM[0] = 30
    INIT_COW_NUM = INIT_NUM[1] = 150
    INIT_GRASS_NUM = INIT_NUM[2] = 500

    def __init__(self, mEnergy, Speed, life, X, Y, cost, rate, type):
        self.energy = mEnergy / 3  # 当前体力值，初始化为最大值的三分之一
        self.maxEnergy = mEnergy  # 最大体力值maxEnergy(?被吃掉的话对面获得哪个呢
        self.speed = Speed  # 移动速度？speed
        self.age = 0  # 目前的年龄age。新开图的话感觉正态分布比较好
        self.lifespan = life  # 最大寿命lifespan
        self.pos = Vector(X, Y)  # Postion 位置坐标
        self.energyCostPerTime = cost  # 单位时间流逝的能量
        self.rate = rate  # 繁殖率
        self.dead = False
        self.type = type
        self.typeStr = Creature.TypeLst[type]

    def __str__(self) -> str:
        return f"{self.typeStr}（位置: {self.pos}，能量：{self.energy}，{'存活' if self.dead==False else '死亡'})"

    # 吃掉食物的函数（能量增长
    # 传入一个被捕食的对象
    def eat(self, eaten):
        eaten.dead = True
        # print(f"{eaten} 被吃")
        self.energy = (
            self.energy + eaten.energy
            if self.energy + eaten.energy < self.maxEnergy
            else self.maxEnergy
        )
        # print(f"捕食者是 {self}")

    # 繁殖函数（应不应该繁殖），对于个体，以一定概率进行繁殖
    def shouldReproduce(self, CreatureLst):
        # if (
        #     self.energy > self.maxEnergy / 3
        #     and self.age > self.lifespan / 5
        #     and random.random() < self.rate
        # ):

        #     # self.energy /= 2  # 若繁殖，则能量减半
        #     return True
        # return False
        NUM_JUDGE = random.random() < (
            1
            / (1 + math.exp(len(CreatureLst[self.type]) - Creature.INIT_NUM[self.type]))
        )

        mapSize = Creature.MAP_SIZE
        edgeSize = Creature.MAP_SIZE // 8

        IN_CORNER = (
            (self.pos.X < edgeSize and self.pos.Y < edgeSize)
            or (self.pos.X >= (mapSize - edgeSize) and self.pos.Y < edgeSize)
            or (self.pos.X < edgeSize and self.pos.Y >= (mapSize - edgeSize))
            or (
                self.pos.X >= (mapSize - edgeSize)
                and self.pos.Y >= (mapSize - edgeSize)
            )
        )

        AROUND_EDGE = (
            self.pos.X < edgeSize
            or self.pos.X >= (mapSize - edgeSize)
            or self.pos.Y < edgeSize
            or self.pos.Y >= (mapSize - edgeSize)
        )

        return NUM_JUDGE and not AROUND_EDGE

    # 若生物存活，则返回 True
    # 若生物死亡（能量为0/寿命达到上限）则返回 False
    def timePass(self):
        self.age += 1
        self.energy -= self.energyCostPerTime
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy
        if self.age > self.lifespan or self.energy <= 0:
            self.dead = True
        return not self.dead

    def isDead(self):
        return self.dead

    # 按平均分布随机设定年龄与能量水平，主要用在初始化的时候
    def randomize(self, ageflag=True, energyflag=True):
        if ageflag:
            # self.age = abs((int)((self.lifespan * random.normalvariate(0.5, 0.5))))
            self.age = int(random.uniform(0, self.lifespan / 2))
        if energyflag:
            # self.energy = abs((int)(self.maxEnergy * random.normalvariate(0.5, 0.5)))
            self.energy = int(random.uniform(self.maxEnergy / 2, self.maxEnergy))
        return self

    def moveTo(self, nextPos: Vector):
        self.pos = nextPos if nextPos is not None else self.pos
        # print(f'--in creature{self.type} move from {self.pos} to {nextPos}')
        # return self
