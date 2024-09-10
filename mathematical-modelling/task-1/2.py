# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

# y^2 = f(x)
def y2(x, C):
    return 3 * x**2 / (2 * np.log(C * x))

def analytical_solution(xs, C):
    # y^2 values for xs
    y2s = y2(xs, C)  

    # we have an expression for y^2 so we need to visualize two branches
    return (-np.sqrt(y2s), np.sqrt(y2s))

# First problem expressed in the form F(x, y) = y'
def model(y, x):
    return y * (3 * x**2 - y**2 ) / (3 * x**3)

# basicly avoid rendering points near y = 0
def find_points_to_render(ys, threshold):
    points_to_include = 0
    for y in ys:
        if np.abs(y) < threshold or np.isnan(y):
            break
        points_to_include = points_to_include + 1
    return points_to_include

cs = [ 0.5, 1, 1.5, 2 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

offsets = [ 2.1, 1.1, 0.7, 0.56 ]

plt.xlim(0, 10)
plt.ylim(-8, 8)

threshold = 0.01

plt.xlabel("x")
plt.ylabel("y")

for c, color, offset in zip(cs, colors, offsets):
    
    # before plotting make sure we don't include if
    # derivative starts to go haywire (in this case where y = 0)
    x_start, x_end, steps = offset, 10, 1000
    xs = np.linspace(x_start, x_end, steps)

    y0 = np.sqrt(y2(xs[0], c))
    ys2_lower, ys2_upper = sc.odeint(model, -y0, xs), sc.odeint(model, y0, xs)
    N, M = find_points_to_render(ys2_lower, threshold), find_points_to_render(ys2_upper, threshold)

    # plot numerical solution branches
    plt.scatter(xs[:N:40], ys2_lower[:N:40], color=color)
    plt.scatter(xs[:M:40], ys2_upper[:M:40], color=color)

    # plot analytical solution branches
    x_start, x_end, steps = 0, 10, 1000
    xs = np.linspace(x_start, x_end, steps)
    ys1_lower, ys1_upper = analytical_solution(xs, c)
    plt.plot(xs, ys1_lower, color=color)
    plt.plot(xs, ys1_upper, color=color)

# %%
