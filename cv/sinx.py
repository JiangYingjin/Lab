# %%
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt


x = np.linspace(0, 2 * np.pi, 1000)
y = np.sin(x)

plt.plot(x, y)
