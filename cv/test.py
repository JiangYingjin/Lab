# %%
from tool import *
import numpy as np
import matplotlib.pyplot as plt


# 定义信号
def rectangular_pulse(t, T):
    return np.where(np.abs(t) <= T / 2, 1, 0)


def cos_signal(t, f):
    return np.cos(2 * np.pi * f * t)


def sin_signal(t, f):
    return np.sin(2 * np.pi * f * t)


def triangular_pulse(t, T):
    return np.where(np.abs(t) <= T / 2, 1 - np.abs(t) / (T / 2), 0)


# 生成时间序列
T = 2 * np.pi
t = np.linspace(-3 * T, 3 * T, 1000)

# 生成信号
signals = [
    rectangular_pulse(t, T),
    cos_signal(t, 3) * rectangular_pulse(t, T),
    sin_signal(t, 3) * rectangular_pulse(t, T),
    3 * triangular_pulse(t, T),
]

# 计算傅里叶级数
fft_results = [np.fft.fftshift(np.fft.fft(signal)) for signal in signals]
frequencies = np.fft.fftshift(np.fft.fftfreq(t.size, d=(t[1] - t[0])))

# 绘制信号及其傅里叶级数
fig, axs = plt.subplots(len(signals), 3, figsize=(15, 10))

for i, (signal, fft_result) in enumerate(zip(signals, fft_results)):
    # 绘制原始信号
    axs[i, 0].plot(t, signal)
    axs[i, 0].set_title(f"Signal {i+1}")
    axs[i, 0].set_xlabel("t")
    axs[i, 0].set_ylabel("Amplitude")

    # 绘制傅里叶变换的幅度谱
    axs[i, 1].plot(frequencies, np.abs(fft_result))
    axs[i, 1].set_title(f"FFT of Signal {i+1}")
    axs[i, 1].set_xlabel("Frequency")
    axs[i, 1].set_ylabel("Amplitude")

    # 绘制傅里叶级数
    axs[i, 2].stem(frequencies, np.abs(fft_result), basefmt=" ")
    axs[i, 2].set_title(f"Fourier Series of Signal {i+1}")
    axs[i, 2].set_xlabel("Frequency")
    axs[i, 2].set_ylabel("Amplitude")

plt.tight_layout()
plt.show()
