
def fractionalKnapsack(goods, remainingWeight):
    Take = [0 for _ in range(len(goods))]
    totalValue = 0
    for index, prize, weight in goods:
        if remainingWeight >= weight:
            Take[index-1] = 1
            totalValue += prize
            remainingWeight -= weight
        else:
            Take[index-1] = remainingWeight / weight
            totalValue += remainingWeight / weight * prize
            remainingWeight = 0
            break
    return totalValue, Take


goods = [(1, 60, 10), (2, 100, 20), (3, 120, 30),
         (4, 150, 40), (5, 90, 30)]  # (index, prize, weight)
goods.sort(key=lambda x: x[1]/x[2], reverse=True)
totalValue, Take = fractionalKnapsack(goods, 50)
print(totalValue, Take)
