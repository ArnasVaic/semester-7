# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

# y^2 = f(x)
def y2(x, C):
    return C * np.exp(-2 * np.arcsin(x / np.sqrt(5))) -2

def analytical_solution(xs, C):
    # y^2 values for xs
    y2s = y2(xs, C)  

    # we have an expression for y^2 so we need to visualize two branches
    return (-np.sqrt(y2s), np.sqrt(y2s))

# First problem expressed in the form F(x, y) = y'
def model(y, x):
    return -(y ** 2 + 2) / (y * np.sqrt(5 - x ** 2))

# basicly avoid rendering points near y = 0
def find_points_to_render(ys, threshold):
    points_to_include = 0
    for y in ys:
        if np.abs(y) < threshold or np.isnan(y):
            break
        points_to_include = points_to_include + 1
    return points_to_include

cs = [ 0.5, 1, 2, 4 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

x_start, x_end, steps = -np.sqrt(5) + 0.01, 2, 1000
xs = np.linspace(x_start, x_end, steps)

plt.xlim(-np.sqrt(5), 1)
plt.ylim(-8, 8)

threshold = 0.01

plt.xlabel("x")
plt.ylabel("y")

for c, color in zip(cs, colors):
    
    # before plotting make sure we don't include if
    # derivative starts to go haywire (in this case where y = 0)
    y0 = np.sqrt(y2(xs[0], c))
    ys2_lower, ys2_upper = sc.odeint(model, -y0, xs), sc.odeint(model, y0, xs)
    N, M = find_points_to_render(ys2_lower, threshold), find_points_to_render(ys2_upper, threshold)

    # plot numerical solution branches
    plt.scatter(xs[:N:20], ys2_lower[:N:20], color=color)
    plt.scatter(xs[:M:20], ys2_upper[:M:20], color=color)

    # plot analytical solution branches
    ys1_lower, ys1_upper = analytical_solution(xs, c)
    plt.plot(xs, ys1_lower, color=color)
    plt.plot(xs, ys1_upper, color=color)

# %%
