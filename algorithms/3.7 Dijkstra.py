inf = float('inf')


def Dijkstra(M: list, start_point):
    V_num = len(M)
    start_point -= 1
    visited = []
    distance = [inf for _ in range(V_num)]
    Path = [[] for _ in range(V_num)]

    def getMinValIdx(distance: list):
        ValIdx = [(i, distance[i]) for i in range(V_num)]
        ValIdx.sort(key=lambda x: x[1])
        print(f'(Weight, Adjacent Vertice) after sorted:')
        strp = ''
        for vertice, weight in ValIdx:
            strp += f'({weight}, {vertice+1}), '
        print(strp.removesuffix(', '))
        for vertice, validMinVal in ValIdx:
            if vertice not in visited:
                print(
                    f"Vertice {vertice+1} hasn't been visited. Selected as the next point.")
                visited.append(vertice)
                return vertice, validMinVal
            print(
                f"Vertice {vertice+1} has been visited. Pass.")

    for _ in range(V_num+1):

        print(f'\n{_}th Iteration:')
        if _ == 0:
            currentVertice = start_point
            currentBaseDistance = 0
        if _ > 0:
            currentVertice, currentBaseDistance = getMinValIdx(distance)
        for vertice in range(V_num):
            if currentBaseDistance + M[currentVertice][vertice] < distance[vertice]:
                distance[vertice] = currentBaseDistance + \
                    M[currentVertice][vertice]
                Path[vertice] = Path[currentVertice]+[vertice+1]

        print(f'Result of {_}th Iteration:')
        print('Distance:', distance)
        print('Path:', Path)

    strp = '\nResult:\n'
    for vertice in range(V_num):
        strp += f'Distance({start_point+1}, {vertice+1}) = {distance[vertice]}. Path: {Path[vertice]}\n'
    print(strp)


M = [
    [0, 5, 7, 12, inf, inf, inf],
    [inf, 0, 1, inf, 6, inf, inf],
    [inf, inf, 0, 1, 5, 10, inf],
    [inf, inf, inf, 0, inf, 13, inf],
    [inf, inf, inf, inf, 0, 2, 7],
    [inf, inf, inf, inf, inf, 0, 3],
    [inf, inf, inf, inf, inf, inf, 0],
]

Dijkstra(M, 1)
