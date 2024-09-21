# %%
import numpy as np
import matplotlib.pyplot as plt

def y(x, C):
    return np.sqrt(C * np.exp(-2 * np.arcsin(x / np.sqrt(5))) - 2)

cs = [ 1, 2, 3, 4 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

plt.xlim(-np.sqrt(5), np.sqrt(5) * np.sin(0.5 * np.log(2)))
plt.ylim(-8, 8)
plt.xlabel("x")
plt.ylabel("y")

for c, color in zip(cs, colors):
    x_start = -np.sqrt(5) + 0.01
    x_end = np.sqrt(5) * np.sin(0.5 * np.log(c / 2))
    xs = np.linspace(x_start, x_end, 1000)
    ys = y(xs, c)
    plt.plot(xs, ys, color=color, label=f'C={c}')
    plt.plot(xs, -ys, color=color)
plt.legend()
# %%
