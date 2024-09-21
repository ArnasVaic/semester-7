# %%
import numpy as np
import matplotlib.pyplot as plt
from sympy import * 

x = symbols('x')
y = Function('y')(x)
equation = Eq(3 * x**3 * y.diff(x), y * (3 * x**2 - y**2))
solutions = dsolve(equation)

cs = [ 0.5, 1, 1.5, 2 ]
colors = [ 'cyan', 'magenta', 'blue', 'red' ]

plt.xlim(0, 4)
plt.ylim(-10, 10)
plt.xlabel("x")
plt.ylabel("y")

for c, color in zip(cs, colors):
    adjusted_c = 2 * np.log(c)
    xs = np.linspace(1/adjusted_c, 4, 1000)
    sol = solutions[0].rhs.subs('C1', adjusted_c)
    ys = np.array([ sol.subs(x, xi).evalf() for xi in xs ])
    plt.plot(xs, ys, color=color, label=f'C={adjusted_c:02f}')
    plt.plot(xs, -ys, color=color)
plt.legend()
# %%
