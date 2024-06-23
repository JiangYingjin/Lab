import random
import numpy as np
from time import time
from AStar import *
from creature import *
from vector import *

# from threading import *
import threading
import multiprocessing

SQRT_2 = 1.4142135623730951
RETRY_TIMES = 2

# 一些固定属性，可慢慢调
# 0-tiger, 1-cow, 2-grass
prop = [
    {"mEnergy": 100, "Speed": 3, "life": 100, "cost": 3, "rate": 0.08},  # 虎
    {"mEnergy": 120, "Speed": 2, "life": 80, "cost": 1, "rate": 0.3},  # 牛
    {"mEnergy": 20, "Speed": 0, "life": 50, "cost": -1, "rate": 0.35},  # 羊
]

mEnergy = 10
emergencyLevel = 500

maxCreatureNum = [300, 1000, 3000]  # 最大物种数量（虎，牛，草）


class Control:
    def __init__(self, map_size):
        self.MAP_SIZE = map_size
        self.BarrierMap = [[0] * self.MAP_SIZE for _ in range(self.MAP_SIZE)]
        self.CreLoc = [
            [[0] * self.MAP_SIZE for _ in range(self.MAP_SIZE)] for _ in range(0, 3)
        ]
        self.CreatureLst = [[], [], []]
        self.spmap = spMap(self.MAP_SIZE, self.BarrierMap)
        self.threads = []

    # 障碍物初始化
    # 定义障碍物 - 可通过传入二维数组_map以设定特定形状的障碍物

    def barrier_init(self, _map):
        # 默认障碍物
        if (type(_map) != type([]) and type(_map) != type(np.array([]))) or np.array(
            _map
        ).size != [self.MAP_SIZE, self.MAP_SIZE]:
            for i in range(int(self.MAP_SIZE / 4), int(self.MAP_SIZE / 2)):
                self.BarrierMap[int(self.MAP_SIZE / 3)][i] = 1
            for i in range(
                int(self.MAP_SIZE / 2), int(self.MAP_SIZE - (self.MAP_SIZE / 4))
            ):
                self.BarrierMap[int(self.MAP_SIZE * 2 / 3)][i] = 1
        # 自定义障碍物
        else:
            self.BarrierMap.copy(_map)

        # 给Map对象更新障碍物
        self.spmap.map = self.BarrierMap

    # 在地图内随机位置生成相应只数的tiger，cow，grass
    def creature_init(self, tiger_num, cow_num, grass_num):
        self.CreatureLst[0].clear()
        self.CreatureLst[1].clear()
        self.CreatureLst[2].clear()
        # 清除位置标记
        for _ in range(0, 3):
            self.ClearPos(_)
        for i in range(0, tiger_num):
            newcre = self.create_new(0, -1, -1)
            # randomize会按正态分布随机设定年龄与能量水平
            if newcre != None:
                self.CreatureLst[0].append(newcre.randomize())
        for i in range(0, cow_num):
            newcre = self.create_new(1, -1, -1)
            # randomize会按正态分布随机设定年龄与能量水平
            if newcre != None:
                self.CreatureLst[1].append(newcre.randomize())
        for i in range(0, grass_num):
            newcre = self.create_new(2, -1, -1)
            # randomize会按正态分布随机设定年龄与能量水平
            if newcre != None:
                self.CreatureLst[2].append(newcre.randomize())
        print("Initialize with numbers")
        print(
            f"In list {len(self.CreatureLst[0])} {len(self.CreatureLst[1])} {len(self.CreatureLst[2])}"
        )
        # self.printmarker(0)
        # self.printmarker(1)
        # self.printmarker(2)

    # 不允许同种生物相互重叠

    def create_new(self, code, X, Y):
        # 若单种生物数量超过地图容量上限则跳过生成新生物
        if len(self.CreatureLst[code]) >= self.MAP_SIZE**2 - np.sum(self.BarrierMap):
            return None
        elif (
            len(self.CreatureLst[code])
            >= (self.MAP_SIZE**2 - np.sum(self.BarrierMap)) * 0.7
        ):
            flag = False
            X = int(random.uniform(0, self.MAP_SIZE))
            Y = int(random.uniform(0, self.MAP_SIZE))
            for i in range(0, self.MAP_SIZE):
                tX = (X + i) % self.MAP_SIZE
                for j in range(0, self.MAP_SIZE):
                    tY = (Y + j) % self.MAP_SIZE
                    if self.isPosValid(Vector(tX, tY), code):
                        flag = True
                        break
                if flag:
                    break
            X, Y = tX, tY
        # tx,ty均为-1时，在地图内随机生成一个编码为code的生物
        elif X == -1 and Y == -1:
            # 生物容量过大时，放弃随机，直接搜索空位生成新生物
            if (
                len(self.CreatureLst[code])
                >= (self.MAP_SIZE**2 - np.sum(self.BarrierMap)) * 0.7
            ):
                flag = False
                X = int(random.uniform(0, self.MAP_SIZE))
                Y = int(random.uniform(0, self.MAP_SIZE))
                for i in range(0, self.MAP_SIZE):
                    tX = (X + i) % self.MAP_SIZE
                    for j in range(0, self.MAP_SIZE):
                        tY = (Y + j) % self.MAP_SIZE
                        if self.isPosValid(Vector(tX, tY), code):
                            flag = True
                            break
                    if flag:
                        break
                X, Y = tX, tY
            # 随机确定一个非障碍的位置，生成新的生物
            else:
                while not self.isPosValid(Vector(X, Y), code):
                    X, Y = (int)(random.uniform(0, self.MAP_SIZE)), (int)(
                        random.uniform(0, self.MAP_SIZE)
                    )
        # tx,ty不均为-1时，在地图内以(tx,ty)为中心，按正态分布概率
        # 确定一个非障碍的位置,随机生成一个编码为code的生物
        else:
            X0, Y0 = X, Y
            retries = 0
            while not self.isPosValid(Vector(X, Y), code) and retries < RETRY_TIMES:
                retries += 1
                X = (int)(X0 + random.normalvariate(0, 0.5) * self.MAP_SIZE * 0.5)
                Y = (int)(Y0 + random.normalvariate(0, 0.5) * self.MAP_SIZE * 0.5)
            if retries >= RETRY_TIMES:
                return None
        # print(f"繁殖 - 母体位置：({X0}, {Y0})，子体位置：({X}, {Y})")
        self.CreLoc[code][Y][X] = 1
        # print(f"new creature {code} at ({X},{Y})")
        newCreature = Creature(
            prop[code]["mEnergy"],
            prop[code]["Speed"],
            prop[code]["life"],
            X,
            Y,
            prop[code]["cost"],
            prop[code]["rate"],
            type=code,
        )

        # print(newCreature)
        return newCreature

    def dayPass(self):
        """
        在用decision决定下一步时，希望获得的返回值是“目标坐标”
        随后根据“目标坐标”，结合生物自身位置、速度，利用A*计算最终位置
        然后在timePass里检查是否饿死/自然死亡
        然后删去已经死亡的生物

        整个过程从tiger->cow->grass进行处理，保证先由高级捕食者将猎物吃掉，
        随后被吃掉的猎物就不需要进行寿命/能量的判定了
        同时先删掉了死去的tiger，那么cow在逃跑时就不会被这些死去的tiger干扰了
        最后的繁殖过程只对现存的生物进行处理，生成的下一代的初始位置是符合以母体生物为中心正态分布的
        """

        # self.printmarker(0)
        # self.printmarker(1)
        # self.printmarker(2)

        def TigerAction(i):
            nextPos = self.CreatureLst[0][i].pos
            nextPos = self.decisionForPredator(
                self.CreatureLst[0][i], self.CreatureLst[1]
            )
            self.CreLoc[0][self.CreatureLst[0][i].pos.Y][
                self.CreatureLst[0][i].pos.X
            ] = 0
            self.CreLoc[0][nextPos.Y][nextPos.X] = 1
            # print(
            #    f"Tiger at ({self.CreatureLst[0][i].pos.X},{self.CreatureLst[0][i].pos.Y}) move to ({nextPos.X},{nextPos.Y})")
            self.CreatureLst[0][i].moveTo(nextPos)

            # print(f"{tiger} 移动到 {nextPos}")

        def CowAction(i):
            if not self.CreatureLst[1][i].dead:
                # nextPos=self.CreatureLst[1][i].pos
                nextPos = self.decisionForPrey(
                    self.CreatureLst[1][i], self.CreatureLst[2], self.CreatureLst[0]
                )
                self.CreLoc[1][self.CreatureLst[1][i].pos.Y][
                    self.CreatureLst[1][i].pos.X
                ] = 0
                self.CreLoc[1][nextPos.Y][nextPos.X] = 1
                # print(
                #    f"Cow at ({self.CreatureLst[1][i].pos.X},{self.CreatureLst[1][i].pos.Y}) move to ({nextPos.X},{nextPos.Y})")
                self.CreatureLst[1][i].moveTo(nextPos)

        # tiger

        def TigerProcess():
            t001 = time()
            tigerNum = len(self.CreatureLst[0])
            for i in range(tigerNum):
                threading.Thread(target=TigerAction, args=(i,)).start()
            temp = []
            for tiger in self.CreatureLst[0]:
                if tiger.timePass():
                    temp.append(tiger)
                else:
                    self.CreLoc[0][tiger.pos.Y][tiger.pos.X] = 0
                    # print(f"Tiger at ({tiger.pos.X},{tiger.pos.Y}) died")
            self.CreatureLst[0] = temp
            # print("tiger 决策耗时：", (time() - t001))

        # cow
        def CowProcess():
            t002 = time()
            cowNum = len(self.CreatureLst[1])
            for i in range(cowNum):
                threading.Thread(target=CowAction, args=(i,)).start()
            temp = []
            for cow in self.CreatureLst[1]:
                if cow.timePass():
                    temp.append(cow)
                else:
                    self.CreLoc[1][cow.pos.Y][cow.pos.X] = 0
                    # print(f"Cow at ({cow.pos.X},{cow.pos.Y}) died")
            self.CreatureLst[1] = temp
            # print("cow 决策耗时：", (time() - t002))

        # grass
        temp = []
        for grass in self.CreatureLst[2]:
            if grass.timePass():
                temp.append(grass)
            else:
                self.CreLoc[2][grass.pos.Y][grass.pos.X] = 0
                # print(f"Grass at ({grass.pos.X},{grass.pos.Y}) died")
        self.CreatureLst[2] = temp
        # 存活的生物进行繁殖

        threading.Thread(target=TigerProcess).start()
        threading.Thread(target=CowProcess).start()
        threading.Thread(target=self.AllCreatureReproduce).start()

    # 对所有生物进行繁殖
    def SingleCreatureReproduce(self, creature_type, CreatureLst):
        def reproduce(creature: Creature):
            if len(self.CreatureLst[creature_type]) >= maxCreatureNum[creature_type]:
                return
            if creature.shouldReproduce(CreatureLst):
                # 最耗时的部分是在 create_new 这里
                newcre = self.create_new(creature.type, creature.pos.X, creature.pos.Y)
                if newcre != None:
                    self.CreatureLst[creature.type].append(newcre)

        if creature_type in [0, 1, 2]:
            for c in self.CreatureLst[creature_type]:
                reproduce(c)

        # for creature in self.CreatureLst[creature_type]:
        # threading.Thread(target=reproduce, args=(creature,)).start()
        #    reproduce(creature)

    def AllCreatureReproduce(self):
        # 次序不限
        self.SingleCreatureReproduce(0, self.CreatureLst)
        self.SingleCreatureReproduce(1, self.CreatureLst)
        self.SingleCreatureReproduce(2, self.CreatureLst)

        # print(
        #     f"tiger:marker{np.sum(self.CreLoc[0])},number{len(self.CreatureLst[0])}")
        # # self.printmarker(0)
        # print(
        #     f"cow:marker{np.sum(self.CreLoc[1])},number{len(self.CreatureLst[1])}")
        # # self.printmarker(1)
        # print(
        #     f"grass:marker{np.sum(self.CreLoc[2])},number{len(self.CreatureLst[2])}")
        # # self.printmarker(2)

    def printmarker(self, code):
        if code not in [0, 1, 2]:
            return
        toprint = []
        for i in range(0, self.MAP_SIZE):
            for j in range(0, self.MAP_SIZE):
                if (self.CreLoc[code][i][j]) == 1:
                    toprint.append((j, i))
        print(toprint)
        toprintcre = []
        for c in self.CreatureLst[code]:
            toprintcre.append((c.pos.X, c.pos.Y))
        print(toprintcre)

    def ClearPos(self, code):
        self.CreLoc[code] = [[0] * self.MAP_SIZE for _ in range(self.MAP_SIZE)]

    def isPosValid(self, pos, creature_type):
        if pos.X < 0 or pos.X >= MAP_SIZE:
            return False
        if pos.Y < 0 or pos.Y >= MAP_SIZE:
            return False
        if self.BarrierMap[pos.Y][pos.X] == 1:
            return False

        if creature_type == 0:  # 老虎
            if self.CreLoc[0][pos.Y][pos.X] == 1:
                return False
        if creature_type == 1:  # 牛
            if self.CreLoc[1][pos.Y][pos.X] == 1:
                return False
            if self.CreLoc[0][pos.Y][pos.X] == 1:
                return False
        if creature_type == 2:  # 草
            if self.CreLoc[2][pos.Y][pos.X] == 1:
                return False
        return True

    # @timeit
    # A* 寻路调用函数
    def findPath(self, startPos: Vector, endPos: Vector, steps):
        self.spmap.setStartEnd(startPos, endPos)
        self.spmap.process()

        if self.spmap.foundEndNode == None:
            # print("没有找到路径")  # 没有找到路径
            return startPos
        else:
            nodes = []
            node = self.spmap.foundEndNode  # 一个结点
            if node == None:
                return startPos
            else:
                while node != None:
                    nodes.append(node)
                    node = node.frontNode  # 之后这里可能可以优化

                for nodeTmp in nodes[::-1]:
                    if nodeTmp.pos == startPos or nodeTmp.pos == endPos:
                        continue
                    # plt.pause(0.05)
                    startPos.X, startPos.Y = nodeTmp.pos.X, nodeTmp.pos.Y

                    if steps == 1:
                        break
                    else:
                        steps -= 1

            # nextPos = nodes[(-1) * steps - 1]
            return Vector(startPos.X, startPos.Y)

    # 创建search list时判断能量是否归零：避免该猎物已经被吃掉
    def decisionForPredator(self, predator: Creature, PreyLst):
        predatorPos = Vector(predator.pos.X, predator.pos.Y)
        predatorSpeed = predator.speed
        eatRange = 2
        predatorVisibleRange = 10
        # 环境内无猎物：随机移动
        if len(PreyLst) == 0:
            nextPos = (
                Vector(*Vector.moveIncrement[random.randint(0, 7)]) * predatorSpeed
                + predatorPos
            )
            retries = 0
            while not self.isPosValid(nextPos, 0) and retries < RETRY_TIMES:
                retries += 1
                nextPos = (
                    Vector(*Vector.moveIncrement[random.randint(0, 7)]) * predatorSpeed
                    + predatorPos
                )
            if retries >= RETRY_TIMES:
                return predatorPos
            return nextPos

        t004 = time()
        preySearchLst = [
            {
                "entity": prey,
                "distance": predatorPos.distance2(prey.pos),
                "huntingTime": predatorPos.distance2(prey.pos)
                / (predator.speed - prey.speed) ** 2,
            }
            for prey in PreyLst
            if prey.pos.inRange(predatorPos, predatorVisibleRange) and prey.energy > 0
        ]

        if len(preySearchLst) == 0:
            nextPos = (
                Vector(*Vector.moveIncrement[random.randint(0, 7)]) * predatorSpeed
                + predatorPos
            )
            retries = 0
            while not self.isPosValid(nextPos, 0) and retries < RETRY_TIMES:
                retries += 1
                nextPos = (
                    Vector(*Vector.moveIncrement[random.randint(0, 7)]) * predatorSpeed
                    + predatorPos
                )
            if retries >= RETRY_TIMES:
                return predatorPos
            return nextPos

        # preySearchLst.sort(key=lambda x: x["distance"])

        # 距离非常近，在捕食范围之内，直接吃就行了。
        # 否则要选择 距离/速度差（即追捕时间）最短的进行追捕
        huntingTime = 9999
        preyToHuntIdx = 0
        for i, item in enumerate(preySearchLst):
            if item["distance"] <= eatRange:
                # print(f'{predator} 吃掉 {item["entity"]}')
                predator.eat(item["entity"])
                # print("创建 preySearchLst 耗时：", (time() - t004)  * 1000)
                return predatorPos
            if item["huntingTime"] < huntingTime:
                huntingTime = item["huntingTime"]
                preyToHuntIdx = i

        # print("创建 preySearchLst 耗时：", (time() - t004)  * 1000)

        t005 = time()
        nextPos = self.findPath(
            predatorPos, preySearchLst[preyToHuntIdx]["entity"].pos, predatorSpeed
        )

        # print("老虎寻路耗时：", (time() - t005)  * 1000)
        # print(
        #     f'{predator} 正在追赶 {preySearchLst[preyToHuntIdx]["entity"]}，其下一步位置是 {nextPos}'
        # )

        # print(f'虎距离牛的距离^2为 {preySearchLst[preyToHuntIdx]["distance"]}')

        if 2 < preySearchLst[preyToHuntIdx]["distance"] <= 9:
            predator.eat(preySearchLst[preyToHuntIdx]["entity"])

        return nextPos

    def decisionForPrey(self, prey: Creature, grassLst: list, PredatorLst: list):
        preyPos = Vector(prey.pos.X, prey.pos.Y)
        preySpeed = prey.speed
        preyEnergy = prey.energy
        range = 7
        predatorSearchLst = []
        dangerLevelLst = []
        predatorDirectionLst = []

        predFlag = False if len(PredatorLst) == 0 else True
        grasFlag = False if len(grassLst) == 0 else True

        # 由于逃跑是基于方向的，因此，先根据逃跑的方向得出一个较近的非障碍物的点，
        # 再对此点进行 A* 寻路
        def escape():
            escapePos = prey.pos.nextPos(escapeDirection, preySpeed + 3, reverse=True)
            # print(f"原位置：{prey.pos}，逃离位置：{escapePos}")
            i = preySpeed
            if escapePos.X >= self.MAP_SIZE:
                # print(f"逃离位置 X 越界")
                escapePos.X = self.MAP_SIZE - 1
            if escapePos.X < 0:
                # print(f"逃离位置 X 越界")
                escapePos.X = 0
            if escapePos.Y >= self.MAP_SIZE:
                # print(f"逃离位置 Y 越界")
                escapePos.Y = self.MAP_SIZE - 1
            if escapePos.Y < 0:
                # print(f"逃离位置 Y 越界")
                escapePos.Y = 0

            # 判断这个点是不是障碍物，如果是的话则要拉远一些距离再得出新的点
            while self.BarrierMap[escapePos.Y][escapePos.X] == 1:
                escapePos = prey.pos.nextPos(
                    escapeDirection, preySpeed + i, reverse=True
                )
                # 极端情况，为了避免程序崩溃，返回 prey 原来的位置，不做任何操作
                if escapePos.X >= self.MAP_SIZE or escapePos.Y >= self.MAP_SIZE:
                    return preyPos
                i += 1

            # 找到了合适的 escapePos，对此进行寻路找到走下一步的点
            # print(f"逃离位置：{escapePos}有效，进行AStar寻路")
            # print(f"猎物速度：{preySpeed}")
            nextPos = self.findPath(preyPos, escapePos, preySpeed)
            # print(f"寻路结果，下一步位置：{nextPos}")
            return nextPos

        # while range < maxRange:
        # 先判断视野范围之内有无捕食者，有的话要记录它们对我的危险程度和方向
        # 后面要求加权矢量和
        if (
            not predFlag
        ):  # 如果没有捕食者就随机移动  就退出 不然死循环 修改测试bylw-------------------------------------
            nextPos = (
                Vector(*Vector.moveIncrement[random.randint(0, 7)]) * preySpeed
                + preyPos
            )
            retries = 0
            while not self.isPosValid(nextPos, 1) and retries < RETRY_TIMES:
                retries += 1
                nextPos = (
                    Vector(*Vector.moveIncrement[random.randint(0, 7)]) * preySpeed
                    + preyPos
                )
            if retries >= RETRY_TIMES:
                return preyPos
            return nextPos

        if predFlag:
            for i, predator in enumerate(PredatorLst):
                # print(predator)
                if prey.pos.inRange(predator.pos, range):
                    dangerLevelLst.append(
                        (prey.speed - predator.speed)
                        / (
                            prey.pos.distance2(predator.pos) + 0.001
                        )  # 防止出现division by zero 修改bylw
                    )
                    predatorDirectionLst.append(prey.pos.direction(predator.pos))

        if not grasFlag:  # 如果草都灭绝了就随机移动
            nextPos = (
                Vector(*Vector.moveIncrement[random.randint(0, 7)]) * preySpeed
                + preyPos
            )
            retries = 0
            while not self.isPosValid(nextPos, 1) and retries < RETRY_TIMES:
                retries += 1
                nextPos = (
                    Vector(*Vector.moveIncrement[random.randint(0, 7)]) * preySpeed
                    + preyPos
                )
            if retries >= RETRY_TIMES:
                return preyPos
            return nextPos

        # 没有危险，牛要找草吃了
        if len(dangerLevelLst) == 0:
            # 体力值都是满的，我睡个觉先
            if preyEnergy == mEnergy:
                return preyPos

            # 不行，还是得找草吃
            elif grasFlag and preyEnergy != mEnergy:
                # 找草
                infinityDistance = 9999
                grassDistance = infinityDistance

                # 所有的草
                for i, grass in enumerate(grassLst):
                    # 视野内的草
                    if prey.pos.inRange(grass.pos, range):
                        # 在牛身旁的草
                        if prey.pos.distance2(grass.pos) <= 2:
                            # 牛原地吃草
                            prey.eat(grass)
                            return prey.pos

                        # 不在我身旁，当我能看到的草。找到最近的草
                        if prey.pos.distance2(grass.pos) < grassDistance**2:
                            grassIdx = i
                            grassDistance = prey.pos.distance2(grass.pos)

                # 说明视野内没发现草，随机移动
                # 牛牛近视了，视野范围太小，找不到草，要扩大视野范围额
                if grassDistance == infinityDistance:
                    nextPos = (
                        Vector(*Vector.moveIncrement[random.randint(0, 7)]) * preySpeed
                        + preyPos
                    )
                    retries = 0
                    while not self.isPosValid(nextPos, 1) and retries < RETRY_TIMES:
                        retries += 1
                        nextPos = (
                            Vector(*Vector.moveIncrement[random.randint(0, 7)])
                            * preySpeed
                            + preyPos
                        )
                    if retries >= RETRY_TIMES:
                        return preyPos
                    return nextPos
                # 找到草了，牛开始寻路
                elif grassDistance < infinityDistance:
                    # print(f"{prey} 想吃草：{grassLst[grassIdx]}")
                    nextPos = self.findPath(preyPos, grassLst[grassIdx].pos, preySpeed)
                    # print(f"猎物速度：{preySpeed}")
                    # print(f"通过AStar找草，下一步：{nextPos}")
                    return nextPos

        # 视野范围之内有捕食者。危险，快跑！
        # 要确定有多危险，便于后面权衡逃跑和吃草。同时确定逃跑的方向
        elif len(dangerLevelLst) != 0:
            # print(f"{prey} 有危险，计算危险水平")
            totalDangerLevel, escapeDirection = Vector.weightedSum(
                dangerLevelLst, predatorDirectionLst, reverse=True
            )

            # 牛牛体力还可以，先不吃草，逃命要紧
            if preyEnergy >= 0.4 * mEnergy:
                # print(f"{prey} 逃跑")
                return escape()

            # 牛牛感觉快不行勒
            elif preyEnergy < 0.4 * mEnergy and grasFlag:
                # 如果危险水平低的话，牛牛假定捕食者不是奔我而来
                # 那么我，先苟活一波，找草吃
                if totalDangerLevel < emergencyLevel:
                    predatorDirectionIdxLst = [
                        (
                            ((direction + Vector.radians202_5) % Vector.radians360)
                            // Vector.radians45
                        )
                        for direction in predatorDirectionLst
                    ]
                    predatorDirectionIdxTmp1Lst = [
                        idx - 1 if idx != 0 else 7 for idx in predatorDirectionIdxLst
                    ]
                    predatorDirectionIdxTmp2Lst = [
                        idx + 1 if idx != 7 else 0 for idx in predatorDirectionIdxLst
                    ]
                    predatorDirectionIdxSet = set(
                        predatorDirectionIdxTmp1Lst + predatorDirectionIdxTmp2Lst
                    )

                    # 四周都有捕食者，哪都没办法跑，留在原地
                    if len(predatorDirectionIdxSet) == 8:
                        # print("四周都有捕食者")
                        return prey.pos

                    # 还有逃跑的余地
                    infinityDistance = 9999
                    grassDistance = infinityDistance

                    # 所有的草
                    for i, grass in enumerate(grassLst):
                        # 视野内的草
                        if prey.pos.inRange(grass.pos, range):
                            # 在牛身旁的草
                            if prey.pos.distance2(grass.pos) <= 2:
                                # 牛原地吃草
                                # print(f"{prey} 原地吃草")
                                prey.eat(grass)
                                return prey.pos

                            # 不在牛身旁，但在牛视野范围内的草，并且符合这样的条件：
                            # 草的方向是安全的方向，没有捕食者在邻近的方向上
                            # 取最近的草
                            if prey.pos.distance2(grass.pos) < grassDistance**2 and (
                                (
                                    (
                                        (
                                            prey.pos.direction(grass.pos)
                                            + Vector.radians202_5
                                        )
                                        % Vector.radians360
                                    )
                                    // Vector.radians45
                                )
                                not in predatorDirectionIdxSet
                            ):
                                grassIdx = i
                                grassDistance = prey.pos.distance2(grass.pos)

                    # 说明视野内没发现草，往安全的方向随机移动
                    # 牛牛近视了，视野范围太小，找不到艹，要扩大视野范围
                    # 不扩大视野范围了，随机移动
                    if grassDistance == infinityDistance:
                        nextPos = (
                            Vector(
                                *Vector.moveIncrement[
                                    random.choice(
                                        list(
                                            set((0, 1, 2, 3, 4, 5, 6, 7)).difference(
                                                predatorDirectionIdxSet
                                            )
                                        )
                                    )
                                ]
                            )
                            * preySpeed
                            + preyPos
                        )
                        retries = 0
                        while not self.isPosValid(nextPos, 1) and retries < RETRY_TIMES:
                            retries += 1
                            nextPos = (
                                Vector(
                                    *Vector.moveIncrement[
                                        random.choice(
                                            list(
                                                set(
                                                    (0, 1, 2, 3, 4, 5, 6, 7)
                                                ).difference(predatorDirectionIdxSet)
                                            )
                                        )
                                    ]
                                )
                                * preySpeed
                                + preyPos
                            )
                        if retries >= RETRY_TIMES:
                            return preyPos
                        return nextPos

                    # 找到草了，牛开始寻路
                    if grassDistance < infinityDistance:
                        nextPos = self.findPath(
                            preyPos, grassLst[grassIdx].pos, preySpeed
                        )
                        # print(
                        # f"{prey} 准备吃 {grassLst[grassIdx]}，其下一步位置是 {nextPos}")
                        return nextPos

                # 情况特别紧急，不吃草，纯逃跑
                elif totalDangerLevel >= emergencyLevel:
                    # print(f"{prey} 逃跑")
                    return escape()

        return prey.pos
