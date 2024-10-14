# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt



def f(t, u):
    return  np.log(2 * u + t) + u #t + 2 * t**2 * np.sin(u)

u_0 = 1
x_0 = 0
x_end = 1
tau = [0.1, 0.05]

plt.xlabel('$x$')
plt.ylabel('$u$')

fig, axes = plt.subplots(2, sharey=True)

for index, tau_i in enumerate(tau):
    if index == 0:
        axes[index].set_title(f'Lygties $u\'=x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$ sprendinys\ngautas pritaikius 4-pakopį Rungės-Kuto metodą')
    N = int((x_end - x_0) / tau_i)
    xs = np.linspace(x_0, 1, N)
    ts, us = rk4(f, x_0, u_0, tau_i, N)
    us_real = odeint(lambda u, t: f(t, u), u_0, xs)
    axes[index].plot(xs, us_real,label=f'Tikslesnis sprendinys, $\\tau={tau_i}$', linestyle='dashed')
    _, us_double_tau = rk4(f, x_0, u_0, 2 * tau_i, N)
    error = np.abs(us_double_tau[-1] - us[-1]) / (2**4 - 1)
    print(error)
    label = f'$u_{{{tau_i}}}, \\vert u({x_end})-u_{{{ tau_i }}}({x_end})\\vert\\approx {error:.04f}$'
    axes[index].plot(xs, us, label=label)
    axes[index].legend()
plt.show()

tau = 0.05
plt.title(f'Lygties $u\'=x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$ skaitinis sprendinys \nintervale $x\\in[0,1]$ gautas pritaikius Rungės-Kuto metodą su žingsniu $\\tau={tau}$')
plt.xlabel('$x$')
plt.ylabel('$u$')

N = int((x_end - x_0) / tau)
xs = np.linspace(x_0, 1, N)

us_3 = rk3(f, x_0, u_0, tau, N)
xs_4, us_4 = rk4(f, x_0, u_0, tau, N)

us_3_double_tau = rk3(f, x_0, u_0, 2 * tau, N)
xs_double_4, us_4_double_tau = rk4(f, x_0, u_0, 2 * tau, N)

error_3_global = np.abs(us_3_double_tau[-1] - us_3[-1]) / (2**3 - 1)
error_4_global = np.abs(us_4_double_tau[-1] - us_4[-1]) / (2**4 - 1)

label = f'$u_{{\\tau}}$ - 3-pakopis, globali paklaida - $\\vert u({x_end})-u_{{{tau}}}({x_end})\\vert\\approx {error_3_global:.04f}$'
plt.plot(xs, us_3, label=label, linestyle='dotted')

label = f'$u_{{\\tau}}$ - 4-pakopis, globali paklaida - $\\vert u({x_end})-u_{{{tau}}}({x_end})\\vert\\approx {error_4_global:.04f}$'
plt.plot(xs_4, us_4, label=label, linestyle='dashed')
    
us_real = odeint(f, u_0, xs, tfirst=True)
plt.plot(xs, us_real,label=f'Tikslesnis sprendinys, $\\tau={tau}$', linestyle='dashed')

plt.legend()
plt.show()
 
error_3_local = np.abs(us_3_double_tau - us_3) / (2**3 - 1)
error_4_local = np.abs(us_4_double_tau - us_4) / (2**4 - 1)

plt.title(f'Lygties $u\'=x+2x^2\\sin u$ su pradine sąlyga $u({x_0})={u_0}$\n skaitinių sprendinių su žingsniu $\\tau={tau}$\n paklaidos priklausomybė nuo $x$ intervale $x\\in[0, 1]$')
label = f'3 - pakopis, $\\frac{{\\vert u_{{{2 * tau}}}(x)-u_{{{tau}}}(x) \\vert}}{{2^3-1}}$'
plt.plot(xs, error_3_local, label=label)
label = f'4 - pakopis, $\\frac{{\\vert u_{{{2 * tau}}}(x)-u_{{{tau}}}(x) \\vert}}{{2^4-1}}$'
plt.plot(xs, error_4_local, label=label)
plt.legend()
plt.xlabel('$x$')
plt.ylabel('$u$')
plt.show()

    # %%
