# %%
VStr = ["S", "A", "B", "C", "D", "E", "F", "G", "T"]

inf = float("inf")
G = [
    [inf, 3, 1, 5, 7, inf, inf, inf, inf],
    [inf, inf, inf, inf, inf, 2, 3, inf, inf],
    [inf, inf, inf, inf, inf, 9, 16, inf, inf],
    [inf, inf, inf, inf, inf, 5, inf, 7, inf],
    [inf, inf, inf, inf, inf, 10, 2, 4, inf],
    [inf, inf, inf, inf, inf, inf, inf, inf, 13],
    [inf, inf, inf, inf, inf, inf, inf, inf, 1],
    [inf, inf, inf, inf, inf, inf, inf, inf, 2],
    [inf, inf, inf, inf, inf, inf, inf, inf, inf],
]


Path = [[[] for _ in range(len(G))] for _ in range(len(G))]


Stage = (0, 1, 1, 1, 1, 2, 2, 2, 3)


def DPShortestPathForward(G, startV, endV):
    if startV == endV:
        return 0, [VStr[endV]]

    strp = f"\nCalculate d({VStr[startV]}, {VStr[endV]})\n"

    stage = Stage[startV]
    internalV = [V for V, nextStage in enumerate(Stage) if nextStage == stage + 1]

    if len(internalV) == 0:
        strp = f"d({VStr[startV]}, {VStr[endV]}) = inf (There's no edge between them)"
        print(strp)
        return inf, []

    lengthAndPath = []

    strp += f"d({VStr[startV]}, {VStr[endV]}) = min" + "{ "
    for V in internalV:
        if V in [startV, endV]:
            strp += f"d({VStr[startV]}, {VStr[endV]}), "

        else:
            strp += f"d({VStr[startV]}, {VStr[V]}) + d({VStr[V]}, {VStr[endV]}), "

        if Path[V][endV] == []:
            VtoEndVLength, VtoEndVPath = DPShortestPathForward(G, V, endV)

            G[V][endV] = VtoEndVLength
            Path[V][endV] = VtoEndVPath

            lengthAndPath.append(
                (G[startV][V] + VtoEndVLength, [VStr[startV]] + VtoEndVPath)
            )

        else:
            lengthAndPath.append(
                (G[startV][V] + G[V][endV], [VStr[startV]] + Path[V][endV])
            )

    strp = strp[:-2] + " }\n"
    strp += f"d({VStr[startV]}, {VStr[endV]}) = min" + "{ "

    for res in lengthAndPath:
        strp += f"{res[0]}({res[1]}), "
    strp = strp[:-2] + " }"

    print(strp)

    lengthAndPath.sort(key=lambda x: x[0])

    print(
        f"d({VStr[startV]}, {VStr[endV]}) = {lengthAndPath[0][0]} ({lengthAndPath[0][1]})"
    )
    return lengthAndPath[0]


def DPShortestPathBackward(G, startV, endV):
    if startV == endV:
        return 0, [VStr[endV]]

    strp = f"\nCalculate d({VStr[startV]}, {VStr[endV]})\n"

    stage = Stage[endV]
    internalV = [V for V, nextStage in enumerate(Stage) if nextStage == stage - 1]

    if len(internalV) == 0:
        strp = f"d({VStr[startV]}, {VStr[endV]}) = inf (There's no edge between them)"
        print(strp)
        return inf, []

    lengthAndPath = []

    strp += f"d({VStr[startV]}, {VStr[endV]}) = min" + "{ "
    for V in internalV:
        if V in [startV, endV]:
            strp += f"d({VStr[startV]}, {VStr[endV]}), "

        else:
            strp += f"d({VStr[startV]}, {VStr[V]}) + d({VStr[V]}, {VStr[endV]}), "

        if Path[startV][V] == []:
            VtoEndVLength, VtoEndVPath = DPShortestPathBackward(G, startV, V)

            G[startV][V] = VtoEndVLength
            Path[startV][V] = VtoEndVPath

            lengthAndPath.append(
                (G[V][endV] + VtoEndVLength, VtoEndVPath + [VStr[endV]])
            )

        else:
            lengthAndPath.append(
                (G[startV][V] + G[V][endV], Path[startV][V] + [VStr[endV]])
            )

    strp = strp[:-2] + " }\n"
    strp += f"d({VStr[startV]}, {VStr[endV]}) = min" + "{ "

    for res in lengthAndPath:
        strp += f"{res[0]}({res[1]}), "
    strp = strp[:-2] + " }"

    print(strp)

    lengthAndPath.sort(key=lambda x: x[0])

    print(
        f"d({VStr[startV]}, {VStr[endV]}) = {lengthAndPath[0][0]} ({lengthAndPath[0][1]})"
    )
    return lengthAndPath[0]


DPShortestPathForward(G, 0, 8)
DPShortestPathBackward(G, 0, 8)
