# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

def y(x):
    return x/2 - 1/4 + 5/4 * np.exp(-2 * x)

def model(y, x):
    return x - 2 * y

plt.xlabel("x")
plt.ylabel("y")
xs = np.linspace(-1, 4, 1000)

ys = sc.odeint(model, y(xs[0]), xs)

plt.scatter(xs[::20], ys[::20], color='blue')
plt.plot(xs, y(xs), color='red')
plt.scatter([0], [1], color='green')
# %%
