# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

def y(x):
    return x/2 - 1/4 + 5/4 * np.exp(-2 * x)

plt.xlabel("x")
plt.ylabel("y")
xs = np.linspace(-1, 4, 1000)
plt.plot(xs, y(xs), color='red', label=f'$y(x)=\\frac{{5}}{{4}}e^{{-2x}}+\\frac{{x}}{{2}}-\\frac{{1}}{{4}}$')
plt.scatter([0], [1], color='blue', label=f'$y(0)=1$')
plt.legend()
# %%
