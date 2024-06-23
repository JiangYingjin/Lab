# %%
import random
from queue import PriorityQueue

strMapping = {
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "8",
    "4": "0",
    "5": "4",
    "6": "7",
    "7": "6",
    "8": "5",
}


def h(strl: str):
    distance = 0
    for currentPos, targetPos in enumerate(strl):
        currX, currY = currentPos % 3, currentPos // 3
        targX, targY = int(targetPos) % 3, int(targetPos) // 3
        distance += abs(currX - targX) + abs(currY - targY)
        # print(currentPos, targetPos)
        # print(currX, targX, currY, targY)
    return distance


def is_solvable(strl: str):
    inv_num = 0
    showStr = "".join([strMapping[s] for s in strl.replace("4", "")])
    # print(strl)
    # print(seq)
    for i in range(1, 8):
        for j in range(i):
            if int(showStr[j]) > int(showStr[i]):
                inv_num += 1
    print(inv_num, inv_num % 2 == 1)
    return inv_num % 2 == 1


def show8Puzzle(strl):
    hVal = h(strl)
    # strl = [dct[strl[i]] for i in range(9)]
    showStr = "".join([strMapping[s] for s in strl])
    print(f"{showStr[:3]}\n{showStr[3:6]}\n{showStr[6:]}\nh: {hVal}\n")


ActionDct = {
    # 上，下，左，右
    0: [0, 1, 0, 1],
    1: [0, 1, 1, 1],
    2: [0, 1, 1, 0],
    3: [1, 1, 0, 1],
    4: [1, 1, 1, 1],
    5: [1, 1, 1, 0],
    6: [1, 0, 0, 1],
    7: [1, 0, 1, 1],
    8: [1, 0, 1, 0],
}

actionCodeStr = ["上", "下", "左", "右"]


def strSwap(strl: str, a, b):
    return (
        strl[:a] + strl[b] + strl[a + 1 : b] + strl[a] + strl[b + 1 :]
        if a < b
        else strl[:b] + strl[a] + strl[b + 1 : a] + strl[b] + strl[a + 1 :]
    )


def Action(strl: str, blankIdx: int, actionCode: int):
    # print(blankIdx, actionCodeStr[actionCode])
    if actionCode == 0:  # 上
        return strSwap(strl, blankIdx, blankIdx - 3)
        # strl[blankIdx], strl[blankIdx - 3] = strl[blankIdx - 3], strl[blankIdx]
    elif actionCode == 1:  # 下
        return strSwap(strl, blankIdx, blankIdx + 3)
        # strl[blankIdx], strl[blankIdx + 3] = strl[blankIdx + 3], strl[blankIdx]
    elif actionCode == 2:  # 左
        return strSwap(strl, blankIdx, blankIdx - 1)
        # strl[blankIdx], strl[blankIdx - 1] = strl[blankIdx - 1], strl[blankIdx]
    elif actionCode == 3:  # 右
        return strSwap(strl, blankIdx, blankIdx + 1)
        # strl[blankIdx], strl[blankIdx + 1] = strl[blankIdx + 1], strl[blankIdx]
    # return strl


cnt = 0
closed = {}


def solve(node: tuple, strategy: str = "DFS"):
    global cnt, open, openpq, closed
    strl: str = node[1][0]
    formerStep: int = node[1][1]
    cnt += 1

    if cnt % 1000 == 0:
        print(cnt)

    closed[strl] = 1

    if strl == "012345678":
        return True

    # if h(strl) == 0:
    #     print("搜索次数:", cnt)
    #     print("移动步数:", formerStep)
    #     return True

    blankIdx = strl.index("4")

    childNodes = []
    for actionCode, valid in enumerate(ActionDct[blankIdx]):
        if valid:
            childNode = Action(strl, blankIdx, actionCode)
            if closed.get(childNode, 0) == 0:
                childNodes.append((h(childNode), (childNode, formerStep + 1)))

    if strategy == "DFS":
        # childNodes.sort(key=lambda x: x[0], reverse=True)
        open.extend(childNodes)
    elif strategy == "BFS":
        childNodes.sort(key=lambda x: x[0])
        open.extend(childNodes)
    elif strategy == "BestFS":
        for childNode in childNodes:
            openpq.put(childNode)
    if strategy == "DFS (heuristic)":
        childNodes.sort(key=lambda x: x[0], reverse=True)
        open.extend(childNodes)

    return False


Initstrl = [str(_) for _ in range(9)]
random.shuffle(Initstrl)
Initstrl = "".join(Initstrl)
print(Initstrl)

show8Puzzle(Initstrl)

found = False

open = [(h(Initstrl), (Initstrl, 0))]
openpq = PriorityQueue()
openpq.put((h(Initstrl), (Initstrl, 0)))

if is_solvable(Initstrl):
    while not found:
        # found = solve(open.pop(-1), strategy="DFS")
        # found = solve(open.pop(0), strategy="BFS")
        # found = solve(open.pop(-1), strategy="DFS (heuristic)")
        found = solve(openpq.get(), strategy="BestFS")
else:
    print("此八数码无解")
