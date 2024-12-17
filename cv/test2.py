# %%
import sympy as sp


def fseries2(fx, x, n):
    # 定义符号变量
    x = sp.symbols("x")
    i = sp.I  # 复数单位

    # 初始化 an 和 f
    an = []
    f = 0

    for ii in range(-n, n + 1):
        # 计算 an
        ann = sp.integrate(fx * sp.exp(i * (-ii) * x), (x, -sp.pi, sp.pi)) / (2 * sp.pi)
        an.append(ann)

        # 构建傅里叶级数
        f += ann * sp.exp(i * ii * x)

    return an, f


# 示例使用
x = sp.symbols("x")
fx = sp.sin(x)  # 你可以根据需要更改这个函数
n = 30  # 你可以根据需要更改这个值

an, f = fseries2(fx, x, n)

print("an:", an)
print("f:", f)
