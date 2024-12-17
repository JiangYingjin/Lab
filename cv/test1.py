#%%
import sympy as sp


def fseries(fx, x, n):
    # 定义符号变量
    x = sp.symbols("x")

    # 计算 a0
    an = [sp.integrate(fx, (x, -sp.pi, sp.pi)) / (2 * sp.pi)]

    # 初始化 bn 和 f
    bn = []
    f = an[0]

    for i in range(1, n + 1):
        # 计算 an 和 bn
        ann = sp.integrate(fx * sp.cos(i * x), (x, -sp.pi, sp.pi)) / sp.pi
        bnn = sp.integrate(fx * sp.sin(i * x), (x, -sp.pi, sp.pi)) / sp.pi

        # 将结果添加到 an 和 bn 列表中
        an.append(ann)
        bn.append(bnn)

        # 构建傅里叶级数
        f += ann * sp.cos(i * x) + bnn * sp.sin(i * x)

    return an, bn, f


# 示例使用
x = sp.symbols("x")
fx = sp.sin(x)  # 你可以根据需要更改这个函数
n = 5  # 你可以根据需要更改这个值

an, bn, f = fseries(fx, x, n)

print("an:", an)
print("bn:", bn)
print("f:", f)
