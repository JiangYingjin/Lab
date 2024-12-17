# %%
import numpy as np
from queue import PriorityQueue

inf = np.inf
pq = PriorityQueue()
minCost = inf
Route = []

G = [
    [inf, 5, 61, 34, 12],
    [57, inf, 43, 20, 7],
    [39, 42, inf, 8, 21],
    [6, 50, 42, inf, 8],
    [41, 26, 10, 35, inf],
]

G = np.array(G)
n = len(G)

print(f"Cost Matrix: \n\n{G}\n")

# Get the reduced matrix and init Cost
initCost = 0
for i in range(n):
    minVal = G[i].min()
    G[i] -= minVal
    initCost += minVal
    print(f"    Row {i+1} minus {minVal}")
print("")
for j in range(n):
    minVal = G[:, j].min()
    G[:, j] -= minVal
    initCost += minVal
    print(f"    Col {j+1} minus {minVal}")
print(f"\nA total cost of {initCost} is subtracted.\n")
print(f"\nReduced Cost Matrix:\n\n{G}")
print(f"\nInitial Lower Bound: {initCost}\n")


def getPath(G):
    candidateMin = []
    for i in range(n):
        j = G[i].argmin()
        # print((i, j), G[i, j])
        tmpRow = np.concatenate((G[i, :j], G[i, j + 1 :]))
        rowMin = tmpRow.min()
        # print(tmpRow, rowMin)
        tmpCol = np.concatenate((G[:i, j], G[i + 1 :, j]))
        colMin = tmpCol.min()
        # print(tmpCol, colMin)
        candidateMin.append(((i, j), rowMin + colMin))
    candidateMin.sort(key=lambda x: x[1], reverse=True)
    candidateMin = [
        candidate
        for candidate in candidateMin
        if G[candidate[0][0], candidate[0][1]] != inf
    ]
    for candidate in candidateMin:
        print(
            f"If path {candidate[0][0]+1}-{candidate[0][1]+1} is excluded, the lower bound will increase {candidate[1]}"
        )
    print(
        f"    Thus path {candidateMin[0][0][0]+1}-{candidateMin[0][0][1]+1} is selected.\nIt can cause the largest increase of lower bound.\n"
    )
    return candidateMin[0]


def extendWithBranch(newCost, row, col, formerG: np.ndarray, formerPath: list):
    newG = formerG.copy()
    newG[selectedRow] = inf
    newG[:, selectedCol] = inf
    newG[selectedCol, selectedRow] = inf
    # print(f'Put {(newCost, "With", row, col, newG, formerPath + [row, col])}')
    print(
        f"Put 'With path {row+1}-{col+1}' into the Priority Queue, whose lower bound is {newCost}"
    )
    pq.put((newCost, "With", row, col, newG, formerPath + [row + 1, col + 1]))


def extendWithoutBranch(newCost, row, col, formerG: np.ndarray, formerPath: list):
    if newCost != inf:
        newG = formerG.copy()
        newG[selectedRow, selectedCol] = inf
        # print(f'Put {(newCost, "Without", row, col, newG, formerPath)}')
        print(
            f"Put 'Without path {row+1}-{col+1}' into the Priority Queue, whose lower bound is {newCost}\n\n"
        )
        pq.put((newCost, "Without", row, col, newG, formerPath))
    else:
        print(
            f"In the current situation, without path {row+1}-{col+1} is due to no solution.\n\n"
        )


def outputPath(Path):
    # Path = [path + 1 for path in Path]
    # print(Path)
    print("The selected paths are")
    for i in range(0, 2 * n, 2):
        print(f"    {Path[i]}-{Path[i+1]}")
    Route = Path[:2]
    Path = Path[2:]
    while len(Path) != 0:
        interNode = Route[len(Route) - 1]
        idx = Path.index(interNode)
        Path.pop(idx)
        nextNode = Path.pop(idx)
        Route.append(nextNode)
        # print("interNode:", interNode, "nextNode:", nextNode)
        # print(Path)
        # print(Route)
    print(f"Thus, the route is {Route}")
    return Route


(selectedRow, selectedCol), LBincr = getPath(G)
extendWithBranch(initCost, selectedRow, selectedCol, G, formerPath=[])
extendWithoutBranch(initCost + LBincr, selectedRow, selectedCol, G, formerPath=[])


while not pq.empty():
    # branchType, row, col, Path 对于下一步求解没有作用，只是用于过程信息存储的
    # 需要用到的是 formerCost, formerG
    formerCost, branchType, row, col, formerG, formerPath = pq.get()

    if len(formerPath) == 2 * n:
        minCost = formerCost
        print("! FOUND a possible route.")
        Route = outputPath(formerPath)
        print(f"The total cost of this route is {minCost}\n")
        continue

    if formerCost > minCost:
        print(
            f"The Node '{branchType} path {row+1}-{col+1}' will not be extended\nSince its lower bound ({formerCost}) is larger than the existing solution ({minCost})\n"
        )

    elif formerCost <= minCost:
        print(
            f"Extend the Node '{branchType} path {row+1}-{col+1}', whose lower bound is {formerCost}"
        )
        (selectedRow, selectedCol), LBincr = getPath(formerG)
        extendWithBranch(formerCost, selectedRow, selectedCol, formerG, formerPath)
        # print(f"formerCost + LBincr:", formerCost + LBincr)
        extendWithoutBranch(
            formerCost + LBincr, selectedRow, selectedCol, formerG, formerPath
        )


print("\nThe branch and bound search is finished.")
print(f"    The optimal route is {Route}\n    The minimun cost is {minCost}")
