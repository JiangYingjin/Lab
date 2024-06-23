# %%


class LCS:
    def __init__(self, S1: str, S2: str) -> None:
        self.S1 = S1
        self.S2 = S2
        self.idx = 0
        self.iterMode = "row"
        self.iter_i = 1
        self.iter_j = 0
        self.M = [[0 for _ in range(len(S2) + 1)] for _ in range(len(S1) + 1)]
        self.Path = [[[] for _ in range(len(S2) + 1)] for _ in range(len(S1) + 1)]
        self.calcMandPath()
        print(
            self.M[len(self.S1)][len(self.S2)],
            self.Path[len(self.S1)][len(self.S2)],
        )
        lcs.printProcess()

    def calcMandPath(self):
        for i in range(1, len(self.S1) + 1):
            for j in range(1, len(self.S2) + 1):
                if self.S1[i - 1] == self.S2[j - 1]:
                    self.M[i][j] = self.M[i - 1][j - 1] + 1
                    self.Path[i][j] = (
                        [
                            formerStr + self.S1[i - 1]
                            for formerStr in self.Path[i - 1][j - 1]
                        ]
                        if self.M[i - 1][j - 1] > 0
                        else [self.S1[i - 1]]
                    )
                else:
                    if self.M[i][j - 1] > self.M[i - 1][j]:
                        self.M[i][j] = self.M[i][j - 1]
                        self.Path[i][j] = self.Path[i][j - 1]
                    elif self.M[i - 1][j] > self.M[i][j - 1]:
                        self.M[i][j] = self.M[i - 1][j]
                        self.Path[i][j] = self.Path[i - 1][j]
                    else:
                        self.M[i][j] = self.M[i][j - 1]
                        self.Path[i][j] = list(
                            set(self.Path[i][j - 1] + self.Path[i - 1][j])
                        )

    def __iter__(self):
        return self

    def iter(self):
        if self.iter_i == len(self.S1) and self.iter_j == len(self.S2):
            self.iterMode = "row"
            self.iter_i = 1
            self.iter_j = 0
            return None
        elif self.iter_i == len(self.S1) and self.iterMode == "col":
            self.iterMode = "row"
            self.iter_j += 1
            self.iter_i = self.iter_j
            # print("Change to Row", (self.iter_i, self.iter_j))
        elif self.iter_j == len(self.S2) and self.iterMode == "row":
            self.iterMode = "col"
            self.iter_j = self.iter_i
            self.iter_i += 1
            # print("Change to Col", (self.iter_i, self.iter_j))
        else:
            if self.iterMode == "row":
                self.iter_j += 1
                # print('Row scan', (self.iter_i, self.iter_j))
            elif self.iterMode == "col":
                self.iter_i += 1
                # print('Col scan', (self.iter_i, self.iter_j))
        return (self.iter_i, self.iter_j)

    def printProcess(self):
        print(
            "Define Li,j as the length of the longest common string of a1,a2,...,ai from String a and b1,b2,...,bj from String b"
        )

        while (res := self.iter()) != None:
            n, m = res[0], res[1]
            strp = f"L{n},{m} = LCS of ("
            for i in range(1, n + 1):
                strp += f"a{i}"
            strp += ", "
            for j in range(1, m + 1):
                strp += f"b{j}"
            strp += f") = LCS of ({self.S1[:n+1]}, {self.S2[:m+1]}) = {self.M[n][m]}"
            if self.M[n][m]!=0:
                strp+=' ('
                for subStr in self.Path[n][m]:
                    strp+=subStr
                    strp+=', '
                strp=strp[:-2]+')'
            print(strp)

    def printIter(self):
        while (res := self.iter()) != None and self.iter_j < 100:
            print(res)
        else:
            return


lcs = LCS("aabcdaef", "beadf")

