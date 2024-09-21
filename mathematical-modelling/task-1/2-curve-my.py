# %%
import numpy as np
import matplotlib.pyplot as plt

def y(x, C):
    return np.sqrt(3/2 * x**2 / np.log(C * x))

cs = [ 0.5, 1, 1.5, 2 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

plt.xlim(0, 4)
plt.ylim(-10, 10)
plt.xlabel("x")
plt.ylabel("y")

for c, color in zip(cs, colors):
    xs = np.linspace(1/c, 4, 10000)
    ys = y(xs, c)
    plt.plot(xs, ys, color=color, label=f'C={c}')
    plt.plot(xs, -ys, color=color)
plt.legend()
# %%
