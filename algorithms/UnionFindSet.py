class UnionFind:

    def __init__(self, element_num=None):
        self.parent = {}
        if element_num is not None:
            for i in range(element_num):
                self.add(i)

    def add(self, x):
        # 如果已经存在则跳过
        if x in self.parent:
            return 
        self.parent[x] = x

    def merge(self, x, y):
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)
        # 查找到两个元素的树根
        x = self.find(x)
        y = self.find(y)
        # 如果相等，说明属于同一个集合
        if x == y:
            return
        elif x < y:
            self.parent[y] = x 
        else:
            self.parent[x] = y

    def find(self, x):
        # 如果father[x] == x，说明x是树根
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    # 判断是否属于同一个集合
    def same(self, x, y):
        return self.find(x) == self.find(y)