# %%
from queue import PriorityQueue

inf = float("inf")

G = {
    0: ((1, 1), (2, 5), (3, 7), (4, 4)),
    1: ((5, 3), (6, 10)),
    2: ((5, 2), (7, 2)),
    3: ((6, 1),),
    4: ((7, 3),),
    5: ((8, 2),),
    6: ((8, 9),),
    7: ((8, 5),),
    8: (),
}


def shortestPath(G, startPoint, endPoint):
    minCost = inf
    pq = PriorityQueue()
    pq.put((0, (startPoint, [startPoint])))

    while not pq.empty():
        formerCost, (extendPoint, formerPath) = pq.get()
        print(
            f"\nSelect v{extendPoint} to extend. Former cost is {formerCost}\n    Former path is {formerPath}"
        )
        # Branch and bound
        if formerCost >= minCost:
            print(
                f"Path cost of extending point is {formerCost}, which is larger then {minCost}.\nNot consider this branch."
            )
            continue
        # Find the target point
        if extendPoint == endPoint:
            minCost = formerCost
            shortestPath = formerPath
            print(
                f"\nFOUND a solution. Total cost is {formerCost}\nPath is {formerPath}\nNow the Min Cost is {minCost}\n\n\nContinue to search."
            )
            continue
        # Add the children in the Priority Queue
        print(f"Add the chidren of v{extendPoint} in the Priority Queue.")
        for point, pathCost in G[extendPoint]:
            print(
                f"    Put v{point} in the Priority Queue. Its total cost is {formerCost+pathCost}"
            )
            pq.put((formerCost + pathCost, (point, formerPath + [point])))

    print(
        f"\nThe search is done.\nShortest Path is {shortestPath}. Min Cost is {minCost}"
    )


shortestPath(G, 0, 8)
