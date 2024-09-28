# %%

import numpy as np

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
# %%

import matplotlib.pyplot as plt

def f(t, u):
    return t + 2 * t**2 * np.sin(u)

u_0 = 0
t_0 = 0
t_end = 1
tau = [0.1, 0.05]

plt.title(f'Lygties $u\'=t+2t^2\\sin u$ su pradine sąlyga $u({t_0})={u_0}$ sprendinys\ngautas pritaikius Rungės-Kuto metodą')
plt.xlabel('$t$')
plt.ylabel('$u$')
for tau_i in tau:
    N = int((t_end - t_0) / tau_i)
    ts = np.linspace(t_0, 1, N)
    us_rk4 = rk4(f, t_0, u_0, tau_i, N)
    us_rk3 = rk3(f, t_0, u_0, tau_i, N)
    plt.scatter(ts, us_rk3, label=f'$u_{{{tau_i}}}$, 3-pakopis')
    plt.plot(ts, us_rk4, label=f'$u_{{{tau_i}}}$, 4-pakopis')
plt.legend()
plt.show()
# %%
