# %%
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# %%

x = sp.symbols('x')
y = sp.Function('y')(x)
eq = sp.Eq(2 + y**2 + sp.Derivative(y, x) * y * sp.sqrt(5 - x**2), 0)
sol = sp.dsolve(eq)

# %%

def y2(x, C):
    return C * np.exp(-2 * np.arcsin(x / np.sqrt(5))) -2

def analytical_solution(xs, C):
    y2s = y2(xs, C)
    # we have an expression for y^2 so we 
    # need to visualize two branches
    return (-np.sqrt(y2s), np.sqrt(y2s))

# %%

cs = [ 2, 3, 4 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

plt.xlim(-np.sqrt(5), np.sqrt(5))
plt.ylim(-8, 8)
plt.xlabel("x")
plt.ylabel("y")

for c, color in zip(cs, colors):
    
    cauchy_solution = [ s.rhs.subs('C1', c) for s in sol ]

    #print(cauchy_solution)

    x_start = -np.sqrt(5) + 0.01
    x_end = np.sqrt(5) * np.sin(np.log(c / 2))
    steps = 1000

    #print(x_start, x_end, steps)

    #[ print(sp.N(s.subs(x, x_start)), sp.N(s.subs(x, x_end))) for s in cauchy_solution ]

    xs = np.linspace(x_start, x_end, steps)

    # before plotting make sure we don't include if
    # derivative starts to go haywire (in this case where y = 0)
    # ys2_upper = np.array([ sol[0].rhs.subs('x', x).subs('C1', c).evalf() for x in xs ])
    # ys2_lower = np.array([ sol[1].rhs.subs('x', x).subs('C1', c).evalf() for x in xs ])

    # plot automatic solution branches
    # plt.scatter(xs[::20], ys2_lower[::20], color=color)
    # plt.scatter(xs[::20], ys2_upper[::20], color=color)

    # plot analytical solution branches
    ys1_lower, ys1_upper = analytical_solution(xs, c)
    plt.plot(xs, ys1_lower, color=color)
    plt.plot(xs, ys1_upper, color=color)
# %%
