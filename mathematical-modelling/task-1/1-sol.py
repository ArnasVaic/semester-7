# %%
from sympy import *
x = symbols('x')
y = Function('y')(x)
equation = Eq(2 + y**2 + y.diff(x) * y * sqrt(5 - x**2), 0)
solutions = dsolve(equation)
display(solutions[0], solutions[1])
# %%
