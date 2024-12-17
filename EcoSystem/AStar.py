import matplotlib.pyplot as plt
import math
from collections import deque
from matplotlib.patches import *
from vector import *


SQRT_2 = math.sqrt(2)


def pow2(a):
    return a * a


# 树结构，用于回溯路径
class Vector2Node:
    pos = None  # 当前的x、y位置
    frontNode = None  # 当前节点的前置节点
    childNodes = None  # 当前节点的后置节点们
    g = 0  # 起点到当前节点所经过的距离
    h = 0  # 启发值
    D = 1

    def __init__(self, pos):
        self.pos = pos
        self.childNodes = []

    def f(self):
        return self.g + self.h

    def calcGH(self, targetPos):
        self.g = self.frontNode.g + math.sqrt(
            pow2(self.pos.X - self.frontNode.pos.X)
            + pow2(self.pos.Y - self.frontNode.pos.Y)
        )
        dx = abs(targetPos.X - self.pos.X)
        dy = abs(targetPos.Y - self.pos.Y)
        self.h = (dx + dy + (SQRT_2 - 2) * min(dx, dy)) * self.D


NEIGHBOR_DISES = [
    Vector(1, 0),
    Vector(1, 1),
    Vector(0, 1),
    Vector(-1, 1),
    Vector(-1, 0),
    Vector(-1, -1),
    Vector(0, -1),
    Vector(1, -1),
]


# 地图
class spMap:
    def __init__(self, msize, map, startPos=None, endPos=None):
        self.setMap(msize, map)  # 地图，0是空位，1是障碍
        self.setStartEnd(startPos, endPos)

    def setMap(self, msize, _map):
        self.mapsize = msize
        self.map = _map

    def setStartEnd(self, startPoint, endPoint):
        self.startPoint = startPoint  # 起始点
        self.endPoint = endPoint  # 终点
        self.tree = None  # 已经搜寻过的节点，是closed的集合
        self.foundEndNode = None  # 寻找到的终点，用于判断算法结束
        self.addNodeCallback = None

    # 判断当前点是否超出范围
    def isOutBound(self, pos):
        return pos.X < 0 or pos.Y < 0 or pos.X >= self.mapsize or pos.Y >= self.mapsize

    # 判断当前点是否是障碍点
    def isObstacle(self, pos):
        return self.map[pos.Y][pos.X] == 1

    # 判断当前点是否已经遍历过
    def isClosedPos(self, pos):
        if self.tree == None:
            return False
        nodes = []
        nodes.append(self.tree)
        while len(nodes) != 0:
            node = nodes.pop()
            if node.pos == pos:
                return True
            if node.childNodes != None:
                for nodeTmp in node.childNodes:
                    nodes.append(nodeTmp)
        return False

    # 获取周围可遍历的邻居节点
    def getNeighbors(self, pos):
        result = []
        for neighborDis in NEIGHBOR_DISES:
            newPos = pos + neighborDis
            if (
                self.isOutBound(newPos)
                or self.isObstacle(newPos)
                or self.isClosedPos(newPos)
            ):
                continue
            result.append(newPos)
        return result

    def process(self):
        # 初始化open集合，并把起始点放入
        willProcessNodes = deque()
        self.tree = Vector2Node(self.startPoint)
        willProcessNodes.append(self.tree)

        counter = 0
        # 开始迭代，直到找到终点，或找完了所有能找的点
        while (
            self.foundEndNode == None and len(willProcessNodes) != 0 and counter <= 300
        ):
            # 寻找下一个最合适的点，这里是最关键的函数，决定了使用什么算法
            counter += 1

            node = self.popLowGHNode(willProcessNodes)

            if self.addNodeCallback != None:
                self.addNodeCallback(node.pos)

            # 获取合适点周围所有的邻居
            neighbors = self.getNeighbors(node.pos)
            for neighbor in neighbors:
                # 初始化邻居，并计算g和h
                childNode = Vector2Node(neighbor)
                childNode.frontNode = node
                childNode.calcGH(self.endPoint)
                node.childNodes.append(childNode)

                # 添加到open集合中
                willProcessNodes.append(childNode)

                # 找到了终点
                if neighbor == self.endPoint:
                    self.foundEndNode = childNode

    # 广度优先，直接弹出先遍历到的节点
    def popLeftNode(self, willProcessNodes):
        return willProcessNodes.popleft()

    # dijkstra，寻找g最小的节点
    def popLowGNode(self, willProcessNodes):
        foundNode = None
        for node in willProcessNodes:
            if foundNode == None:
                foundNode = node
            else:
                if node.g < foundNode.g:
                    foundNode = node
        if foundNode != None:
            willProcessNodes.remove(foundNode)
        return foundNode

    # A*，寻找f = g + h最小的节点
    def popLowGHNode(self, willProcessNodes):
        foundNode = None
        for node in willProcessNodes:
            if foundNode == None:
                foundNode = node
            else:
                if node.f() < foundNode.f():
                    foundNode = node
        if foundNode != None:
            willProcessNodes.remove(foundNode)
        return foundNode


# 这个文件里面的内容已经全部移动到 Control 中

"""
def findPathShow(x1, y1, x2, y2, steps):
    startPoint = Vector(x1, y1)
    endPoint = Vector(x2, y2)
    map1 = Map(startPoint, endPoint)

    # 障碍物坐标一直不变的，在这里设置，值为1的格子代表有障碍
    for i in range(2, 12):
        map1.map[10][i] = 1
    for i in range(10, 19):
        map1.map[13][i] = 1

    ax = plt.gca()
    ax.set_xlim([0, MAP_SIZE])
    ax.set_ylim([0, MAP_SIZE])

    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            if map1.map[y][x] == 0:
                ax.add_patch(GetBackGroundGrid(x, y))
            else:
                ax.add_patch(GetObstacleGrid(x, y))

    ax.add_patch(GetStartEndGrid(map1.startPoint.X, map1.startPoint.Y))
    ax.add_patch(GetStartEndGrid(map1.endPoint.X, map1.endPoint.Y))

    plt.ion()

    def AddPathGrid(pos):
        if pos == endPoint or pos == startPoint:
            return
        # plt.pause(0.05)

        # 下面这步是显示搜索过的点的范围，用绿色标记
        # ax.add_patch(GetPathGrid(pos.x, pos.y))

    map1.addNodeCallback = AddPathGrid
    map1.process()
    if map1.foundEndNode == None:
        print("No path found")
        # 没有找到路径，随机行走，这个有待补充

    else:
        nodes = []
        node = map1.foundEndNode
        while node != None:
            nodes.append(node)
            node = node.frontNode

        for nodeTmp in nodes[::-1]:
            if nodeTmp.pos == startPoint or nodeTmp.pos == endPoint:
                continue
            # plt.pause(0.05)
            ax.add_patch(GetFoundPathGrid(nodeTmp.pos.X, nodeTmp.pos.Y))
            ax.add_patch(GetBackGroundGrid(x1, y2))
            x1, y1 = nodeTmp.pos.X, nodeTmp.pos.Y
            startPoint = Vector(x1, y1)
            ax.add_patch(GetStartEndGrid(map1.startPoint.X, map1.startPoint.Y))

            ax.add_patch(GetStartEndGrid(map1.endPoint.X, map1.endPoint.Y))
            # plt.pause(0.05)
            if steps == 1:
                break
            else:
                steps -= 1
    return x1, y1, x2, y2
"""

# 这里测试，前面两个数是起点坐标，后面两个数是终点坐标

# test = findPath(Vector(5, 5), Vector(3, 17), 5)
# print(test)

# test = findPath(5, 5, 3, 17, 5)
# test = findPath( 3, 17,5, 5, 8)
# 这里会返回走完第一步之后两者的位置
# plt.ioff()
# plt.show()
