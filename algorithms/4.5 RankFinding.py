# %%
import random
import time
import matplotlib.pyplot as plt


class RankFind:
    def __init__(self, Points: list, type) -> None:
        self.Points = Points
        self.Rank = {}
        if type == "divide-and-conquer":
            Points.sort(key=lambda x: x[0])
            self.divideAndConquerRF(self.Points)
        elif type == "straightforward":
            self.straightforwardRF()
        else:
            raise TypeError
        print(f"Rank of all points:\n\t{self.Rank}")

    def divideAndConquerRF(self, Points):
        if len(Points) == 1:
            self.Rank[Points[0]] = 0

        elif len(Points) > 1:
            print(f"Before dividing:\n\t{Points}")
            A = Points[: len(Points) // 2]
            B = Points[len(Points) // 2 :]
            print(f"After dividing:\n\tA: {A}\n\tB: {B}\n")

            self.divideAndConquerRF(A)
            self.divideAndConquerRF(B)

            print(f"Merging A: {A} and B: {B}:")
            for point in B:
                for cmp_point in A:
                    if cmp_point[0] < point[0] and cmp_point[1] < point[1]:
                        self.Rank[point] += 1
                        print(
                            f"\t{point} dominates {cmp_point}. Rank of {point} adds one to {self.Rank[point]}."
                        )
                    else:
                        print(
                            f"\t{point} cannot dominate {cmp_point}. Rank of {point} remains {self.Rank[point]}."
                        )
            print("\n")

    def straightforwardRF(self):
        for point in self.Points:
            self.Rank[point] = 0
            for cmp_point in self.Points:
                if cmp_point[0] < point[0] and cmp_point[1] < point[1]:
                    self.Rank[point] += 1

    def __str__(self) -> str:
        return str(self.Rank)


Points = [
    (1, 2),
    (5, 6),
    (7, 2),
    (4, 6),
    (10, 10),
    (3, 9),
    (5, 2),
    (3, 5),
    (4, 1),
]

# %%
scaleSet = [200 * i for i in range(1, 11)]
divideAndConquerTime = []
straightforwardTime = []

for scale in scaleSet:
    # Points = list(
    #     set([(random.randint(0, 1e5), random.randint(0, 1e5)) for _ in range(scale)])
    # )
    Points = [(random.randint(0, 1e5), random.randint(0, 1e5)) for _ in range(scale)]
    t1 = time.time()
    RF1 = RankFind(Points, type="divide-and-conquer")
    t2 = time.time()
    RF2 = RankFind(Points, type="straightforward")
    t3 = time.time()
    print(scale)
    divideAndConquerTime.append((t2 - t1))
    straightforwardTime.append((t3 - t2))


plt.plot(scaleSet, divideAndConquerTime)
plt.plot(scaleSet, straightforwardTime)
plt.legend(("Divide and Conquer", "Straightforward"))
plt.xlabel("Scale")
plt.ylabel("Consumption Time (s)")

# %%

Points = list(
    set([(random.randint(0, 100), random.randint(0, 100)) for _ in range(20)])
)
RF = RankFind(Points, type="divide-and-conquer")
print(RF.Points)
print(RF.Rank)
