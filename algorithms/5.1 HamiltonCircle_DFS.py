# %%
G = {
    1: (3, 6),
    2: (3, 7),
    3: (1, 4, 6),
    4: (3, 5, 6),
    5: (4, 6, 7),
    6: (1, 3, 4, 5, 7),
    7: (2, 5, 6),
}

visited = []
Path = []


def DFS(startPoint):
    print(f"    Visit {startPoint}")
    visited.append(startPoint)
    print(f"Now the path is {visited}")

    if len(visited) == len(G):
        if visited[0] in G[visited[-1]]:
            print(f"\n √ FOUND a Hamilton Circle: {visited}\n")
            Path.append(visited.copy())
            return
        else:
            print(
                f"\n ! End point {visited[-1]} is not adjacent to start point {visited[0]}.\n ! Path {visited} can't form a circle.\n"
            )
            return

    for point in G[startPoint]:
        if point not in visited:
            DFS(point)
            print(f"    Pop out {visited[-1]}")
            visited.pop()
            print(f"Now the path is {visited}")
    return


DFS(startPoint=7)
print(f"\n\nDepth-First Search is finished.\nResult: {Path}")


# %%


def dfs_hamiltonian(graph, visited, path, start):
    visited[start] = True
    path.append(start)
    if len(path) == len(graph):  # 所有节点都已经访问
        if path[-1] in graph[path[0]]:  # 最后一个节点是否与开始节点相邻
            return path
    for v in graph[start]:
        if not visited[v]:
            res = dfs_hamiltonian(graph, visited, path, v)  # 继续搜索下一个节点
            if res:
                return res
    visited[start] = False
    path.pop()
    return None


def find_hamiltonian_path(graph):
    visited = {v: False for v in graph}
    path = []
    res = None
    for start in graph:
        res = dfs_hamiltonian(graph, visited, path, start)
        if res:
            break
    return res
