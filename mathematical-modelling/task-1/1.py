# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

def analytical_solution(xs, C):
    solution = np.sqrt(-2 + C * np.exp(-2 * np.arcsin(xs / np.sqrt(5))))    
    # we have an expression for y^2 so we need to visualize two branches
    return (-solution, solution)

# First problem expressed in the form F(x, y) = y'
def model(x, y):
    return -(y ** 2 + 2) / (y * np.sqrt(5 - x ** 2))

cs = [ 0.25, 0.5, 0.75, 1 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

x_start, x_end, steps = -np.sqrt(5), 0, 1000
xs = np.linspace(x_start, x_end, steps)

xs_reversed = xs.flip()

plt.xlim(x_start, x_end)

for c, color in zip(cs, colors):
    (ys1_lower, ys1_upper) = analytical_solution(xs, c)
    
    zip(xs, ys1_lower) + zip()
    
    plt.plot(xs, ys1_lower, color=color)
    plt.plot(xs, ys1_upper, color=color)

# %%
