# %%
from timeit import default_timer as timer

inf = float("inf")

G = [
    [inf, 2, 3, 4, inf, inf, inf],
    [inf, inf, 3, inf, 2, inf, inf],
    [inf, inf, inf, inf, 2, 2, inf],
    [inf, inf, inf, inf, inf, 2, inf],
    [inf, inf, inf, inf, inf, 1, 3],
    [inf, inf, inf, inf, inf, inf, 5],
    [inf, inf, inf, inf, inf, inf, inf],
]

VStr = ["S", "V1", "V2", "V3", "V4", "V5", "T"]
initV, targetV = 0, 6


def Search(strategy="DFS"):
    searching = [(initV, [VStr[initV]], 0)]
    res = []
    strategyDct = {"DFS": -1, "BFS": 0}

    t = timer()
    while len(searching):
        # Start extending the point
        currV, path, formerCost = searching.pop(strategyDct[strategy])

        # Check if it is the target node
        if currV == targetV:
            print(
                f"\nExtend {VStr[currV]}. Reach target node. \nThe path is {path}. Total cost is {formerCost}."
            )
            res.append((path, formerCost))
            continue

        print(f"\nExtend node {VStr[currV]}")

        # If not the target node, searching its child node
        for childV, weight in enumerate(G[currV]):
            if weight != inf:
                print(f"  Add childNode {VStr[childV]} to the searching list")
                searching.append((childV, path + [VStr[childV]], formerCost + weight))

    print("\nEnd of all branch Searching.")
    res.sort(key=lambda x: x[1])
    print(f"\nAll searching result:\n{res}")
    print(f"\nShortest Path: {res[0][0]}\nMinimum Cost: {res[0][1]}")
    print(f"Running time: {(timer()-t):.4f} s")

Search(strategy="DFS")
Search(strategy="BFS")