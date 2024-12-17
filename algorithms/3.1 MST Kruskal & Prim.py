# %%
import time

edges = [
    [1, 2, 10],
    [1, 4, 30],
    [1, 5, 45],
    [2, 3, 50],
    [2, 5, 40],
    [2, 6, 25],
    [3, 5, 35],
    [3, 6, 15],
    [4, 6, 20],
    [5, 6, 55],
]


class UnionFind:
    def __init__(self, element_num=None):
        self.parent = {}
        if element_num is not None:
            for i in range(1, element_num + 1):
                self.add(i)

    def add(self, x):
        if x in self.parent:
            return
        self.parent[x] = x

    def union(self, x, y):
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        elif x < y:
            self.parent[y] = x
        else:
            self.parent[x] = y

    def find(self, x):
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def same(self, x, y):
        return self.find(x) == self.find(y)


def KruskalMST(edges: list):
    t = time.time()

    edges.sort(key=lambda x: x[1])
    edges.sort(key=lambda x: x[0])
    edges.sort(key=lambda x: x[2])
    strp = "\nSorted Edges ((u, v), w):\n"
    for u, v, w in edges:
        strp += f"(({u}, {v}), {w})\n"
    print(strp)

    disjoinset = UnionFind(6)
    MST = []
    MST_weight = 0
    for u, v, w in edges:
        if disjoinset.same(u, v):
            print(f"(({u}, {v}), {w}) forms a cycle. Reject.")
            continue
        disjoinset.union(u, v)
        MST.append((u, v, w))
        MST_weight += w
        print(f"(({u}, {v}), {w}) is added.")
    strp = "\nMST: {"
    for edge in MST:
        u, v, w = edge
        strp += f"(({u}, {v}), {w}), "
    strp = strp.removesuffix(", ") + "}"
    print(strp)
    print(f"Weight of the MST: {MST_weight}")
    print(f"Running time: {time.time()-t:.4f} s")


def PrimMST(edges: list):
    t = time.time()

    V = set()
    for edge in edges:
        V.add(edge[0])
        V.add(edge[1])
    A = set()
    B = V

    MST = []

    print(f"A = {A}  B = {B}\n")
    print("Sorting all edges")

    edges.sort(key=lambda x: x[1])
    edges.sort(key=lambda x: x[0])
    edges.sort(key=lambda x: x[2])

    strp = "Sorted Edges ((u, v), w):\n"
    for u, v, w in edges:
        strp += f"  (({u}, {v}), {w})\n"
    print(strp)

    print(
        f"Add the initial locally optimal edge {((edges[0][0],edges[0][1]),edges[0][2])} into MST"
    )

    def renewPointSet(edge: list):
        if len(B) != 0:
            edges.remove(edge)
            MST.append(edge)
            u, v, w = edge
            formerA = A.copy()
            A.add(u)
            A.add(v)
            diffSet = A.difference(formerA)
            B.difference_update(diffSet)
            strp = "Renew set A and set B\n"
            strp += f"  A = A + {diffSet} = {A}\n"
            strp += f"  B = B - {diffSet} = {B}\n"
            print(strp)

    renewPointSet(edges[0])

    while len(B):
        print("Sorting all possible edges")
        tmpE = [edge for edge in edges if (edge[0] in A and edge[1] not in A) or (edge[0] not in A and edge[1] in A)]
        strp = "Sorted Edges ((u, v), w):\n"
        for u, v, w in tmpE:
            strp += f"  (({u}, {v}), {w})\n"
        print(strp)

        print(
            f"Add the initial locally optimal edge {((tmpE[0][0],tmpE[0][1]),tmpE[0][2])} into MST"
        )

        renewPointSet(tmpE[0])

    MST_weight = 0
    strp = "\nMST: {"
    for edge in MST:
        u, v, w = edge
        MST_weight += w
        strp += f"(({u}, {v}), {w}), "
    strp = strp.removesuffix(", ") + "}"
    print(strp)
    print(f"Weight of the MST: {MST_weight}")
    print(f"Running time: {time.time()-t:.4f} s")


KruskalMST(edges)
PrimMST(edges)
