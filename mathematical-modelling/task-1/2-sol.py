# %%
from sympy import *
x = symbols('x')
y = Function('y')(x)
equation = Eq(3 * x**3 * y.diff(x), y * (3 * x**2 - y**2))
solutions = dsolve(equation)
display(solutions[0], solutions[1])
# %%
