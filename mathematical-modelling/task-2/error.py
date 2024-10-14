# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from solver import rk3, rk4

def f(t, u):
    return t + 2 * t ** 2 * np.sin(u)

u_0 = -1
x_0 = 0
x_end = 1
tau = 0.05

N = int((x_end - x_0) / tau) + 1
M = int((x_end - x_0) / (2 * tau)) + 1

_, us_3 = rk3(f, x_0, u_0, tau, N)
xs, us_3_2tau = rk3(f, x_0, u_0, 2 * tau, M)

_, us_4 = rk4(f, x_0, u_0, tau, N)
_, us_4_2tau = rk4(f, x_0, u_0, 2 * tau, M)

error_rk3 = np.abs(us_3_2tau - us_3[::2]) / (2**3 - 1)
error_rk4 = np.abs(us_4_2tau - us_4[::2]) / (2**4 - 1)

plt.title(
f"""Lygties $u\'=x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$
skaitinių sprendinių su žingsniu $\\tau={tau}$
paklaidos priklausomybė nuo $x$ intervale $x\\in[0, 1]$""")

label = f'3 - pakopis, $\\frac{{\\vert u_{{{2 * tau}}}(x)-u_{{{tau}}}(x) \\vert}}{{2^3-1}}$'
plt.plot(xs, error_rk3, label=label)

label = f'4 - pakopis, $\\frac{{\\vert u_{{{2 * tau}}}(x)-u_{{{tau}}}(x) \\vert}}{{2^4-1}}$'

plt.plot(xs, error_rk4, label=label)
plt.legend()
plt.xlabel('$x$')
plt.ylabel('$u$')

plt.gca().set_ylim((0, 0.00001))
plt.gca().set_xlim((-0.05, x_end+0.05))

plt.show()
# %%
