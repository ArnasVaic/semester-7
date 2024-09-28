# %%

import numpy as np
import matplotlib.pyplot as plt

def rk3(f, t_0, y_0, tau, N):
    t_current = t_0
    y_current = y_0

    ys = np.zeros(N)

    for i in range(N):
        k1 = f(t_current, y_current)
        k2 = f(t_current + tau, y_current + tau * k1)
        k3 = f(t_current + tau/2, y_current + tau/2 * (k1 + k2)/2 )
        
        t_current = t_current + tau
        y_current = y_current + tau/6 * (k1 + k2 + 4*k3)
        ys[i] = y_current
    return ys

def rk4(f, t_0, y_0, tau, N):

    t_current = t_0
    y_current = y_0

    ys = np.zeros(N)

    for i in range(N):
        k1 = f(t_current, y_current)
        k2 = f(t_current + tau/2, y_current + tau/2 * k1)
        k3 = f(t_current + tau/2, y_current + tau/2 * k2)
        k4 = f(t_current + tau, y_current + tau * k3)

        t_current = t_current + tau
        y_current = y_current + tau/6 * (k1 + 2*k2 + 2*k3 + k4)
        ys[i] = y_current
    return ys

def f(t, u):
    return t + 2 * t**2 * np.sin(u)

u_0 = -1
t_0 = 0
t_end = 1
tau = [0.1, 0.05]

plt.title(f'Lygties $u\'=t+2t^2\\sin u$ su pradine sąlyga $u({t_0})={u_0}$ sprendinys\ngautas pritaikius 4-pakopį Rungės-Kuto metodą')
plt.xlabel('$t$')
plt.ylabel('$u$')

for tau_i in tau:
    N = int((t_end - t_0) / tau_i)
    ts = np.linspace(t_0, 1, N)
    us= rk4(f, t_0, u_0, tau_i, N)
    us_double_tau = rk4(f, t_0, u_0, 2 * tau_i, N)
    error = np.abs(us_double_tau[-1] - us[-1]) / (2**4 - 1)
    label = f'$u_{{{tau_i}}}, \\vert u({t_end})-u_{{{ tau_i }}}({t_end})\\vert\\approx {error:.04f}$'
    plt.plot(ts, us, label=label)
    
plt.legend()
plt.show()

tau = 0.1
plt.title(f'Lygties $u\'=t+2t^2\\sin u$ su pradine sąlyga $u({t_0})={u_0}$ sprendinys\ngautas pritaikius Rungės-Kuto metodą su žingsniu $\\tau={tau}$')
plt.xlabel('$t$')
plt.ylabel('$u$')

N = int((t_end - t_0) / tau)
ts = np.linspace(t_0, 1, N)

us_3 = rk3(f, t_0, u_0, tau, N)
us_4 = rk4(f, t_0, u_0, tau, N)

us_3_double_tau = rk3(f, t_0, u_0, 2 * tau, N)
us_4_double_tau = rk4(f, t_0, u_0, 2 * tau, N)

error_3 = np.abs(us_3_double_tau[-1] - us_3[-1]) / (2**3 - 1)
error_4 = np.abs(us_4_double_tau[-1] - us_4[-1]) / (2**4 - 1)

label = f'$u_{{\\tau}}$ - 3-pakopis, $\\vert u({t_end})-u_{{{tau_i}}}({t_end})\\vert\\approx {error_3:.04f}$'
plt.plot(ts, us_3, label=label)
label = f'$u_{{\\tau}}$ - 4-pakopis, $\\vert u({t_end})-u_{{{tau_i}}}({t_end})\\vert\\approx {error_4:.04f}$'
plt.plot(ts, us_4, label=label)
    
plt.legend()
plt.show()

# %%
