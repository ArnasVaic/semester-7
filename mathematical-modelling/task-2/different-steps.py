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

fig, axes = plt.subplots(2, sharey=True)

fig.suptitle(f'Lygties $u\' =x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$ sprendinys\ngautas pritaikius 4-pakopį Rungės-Kuto metodą')

plt.xlabel('$x$')
plt.ylabel('$u$')

for index, tau in enumerate([0.1, 0.05]):

    N = int((x_end - x_0) / tau) + 1
    M = int((x_end - x_0) / (2 * tau)) + 1

    xs, us = rk4(f, x_0, u_0, tau, N)

    _, us_2tau = rk4(f, x_0, u_0, 2 * tau, M)
    error = np.abs(us_2tau[-1] - us[-1]) / (2**4 - 1)
    label = f'$u_{{{tau}}}, \\vert u({x_end})-u_{{{ tau }}}({x_end})\\vert\\approx {error:.2e}$'
    axes[index].plot(xs, us, label=label, color='red')

    us_real = odeint(f, u_0, xs, tfirst=True)
    label = f'Tikslesnis sprendinys, $\\tau={tau}$'
    axes[index].plot(xs, us_real,label=label, linestyle='dotted', color='blue')

    axes[index].set_xlim((-0.05, x_end+0.05))

    axes[index].legend()

fig.subplots_adjust(wspace=0.2)

plt.show()
# %%
