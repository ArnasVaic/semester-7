# %%

from sympy import *
t = symbols('t')
x = Function('x')(t)
equation = Eq(x.diff(t, 2) + 9*x, 4 * sin(t) - cos(4 * t))
general_solution = dsolve(equation, x).rhs
conditions = [
    Eq(general_solution.subs(t, 0), 0),
    Eq(general_solution.diff(t).subs(t, 0), 1)
]
C_values = solve(conditions, symbols("C1, C2"))
general_solution.subs(C_values)

# %%
