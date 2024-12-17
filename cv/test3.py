# %%
import numpy as np
from scipy.integrate import quad


def fseries2(fx, n):
    # 定义积分的上下限
    a, b = -np.pi, np.pi

    # 初始化 an 和 f
    an = []
    f = 0

    def integrand_real(x, ii):
        return fx(x) * np.cos(ii * x)

    def integrand_imag(x, ii):
        return fx(x) * np.sin(ii * x)

    for ii in range(-n, n + 1):
        # 计算 an
        real_part = quad(integrand_real, a, b, args=(ii,))[0] / (2 * np.pi)
        imag_part = quad(integrand_imag, a, b, args=(ii,))[0] / (2 * np.pi)
        ann = real_part + 1j * imag_part
        an.append(ann)

        # 构建傅里叶级数
        f += ann * np.exp(1j * ii * np.linspace(a, b, 1000))

    return an, f


# 示例使用
fx = lambda x: np.sin(x)  # 你可以根据需要更改这个函数
n = 30  # 你可以根据需要更改这个值

an, f = fseries2(fx, n)

print("an:", an)
print("f:", f)
