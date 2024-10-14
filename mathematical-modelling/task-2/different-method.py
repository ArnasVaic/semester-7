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

plt.title(f"""Lygties $u\'=x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$ 
skaitinis sprendinys intervale $x\\in[0,1]$ 
gautas pritaikius Rungės-Kuto metodą su žingsniu $\\tau={tau}$""")

plt.xlabel('$x$')
plt.ylabel('$u$')

N = int((x_end - x_0) / tau) + 1
M = int((x_end - x_0) / (2 * tau)) + 1

xs, us_3 = rk3(f, x_0, u_0, tau, N)

label = f'Tikslesnis sprendinys, $\\tau={tau}$'
us_real = odeint(f, u_0, xs, tfirst=True)
plt.plot(xs, us_real,label=label, linewidth=4, color='green')

_, us_3_2tau = rk3(f, x_0, u_0, 2 * tau, M)
error_3_global = np.abs(us_3_2tau[-1] - us_3[-1]) / (2**3 - 1)
label = f'$u_{{\\tau}}$ - 3-pakopis, globali paklaida - $\\vert u({x_end})-u_{{{tau}}}({x_end})\\vert\\approx {error_3_global:.2e}$'
plt.plot(xs, us_3, label=label, marker='D', color='red')

_, us_4 = rk4(f, x_0, u_0, tau, N)
_, us_4_2tau = rk4(f, x_0, u_0, 2 * tau, M)
error_4_global = np.abs(us_4_2tau[-1] - us_4[-1]) / (2**4 - 1)
label = f'$u_{{\\tau}}$ - 4-pakopis, globali paklaida - $\\vert u({x_end})-u_{{{tau}}}({x_end})\\vert\\approx {error_4_global:.2e}$'
plt.plot(xs, us_4, label=label, marker='x', color='yellow')

plt.gca().set_xlim((-0.05, x_end+0.05))

plt.legend()
plt.show()
# %%
