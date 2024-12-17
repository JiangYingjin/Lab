#%%
import numpy as np
import matplotlib.pyplot as plt

# 生成包含噪声的实数序列
x = np.linspace(0, 6 * np.pi, 201)
y = np.sin(5 * x) + np.random.normal(0, 0.1, 201)

print(len(x), len(y))

# 进行FFT变换
rfft_y = np.fft.rfft(y)

# 提取低频部分
rfft_y[30:] = 0

# 进行IFFT逆变换
irfft_y = np.fft.irfft(rfft_y,n=201)

# 绘制原始信号、滤波后的信号和滤波器的频率响应
plt.subplot(2, 1, 1)
plt.plot(x, y)
plt.title("Original signal")

plt.subplot(2, 1, 2)
plt.plot(x, irfft_y)
plt.title("Filtered signal")

plt.show()
