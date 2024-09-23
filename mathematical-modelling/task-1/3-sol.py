# %%
from sympy import *
x = symbols('x')
y = Function('y')(x)
equation = Eq(y.diff(x) + 2 * y,x)
general_solution = dsolve(equation)
constants = solve(general_solution.rhs.subs(x, 0) - 1)
general_solution.subs('C1', constants[0])
# %%
