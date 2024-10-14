import numpy as np

def rk3(f, t_0, y_0, tau, N):
    ts = np.linspace(t_0, t_0 + (N - 1) * tau, N)
    ys = np.zeros(N)
    ys[0] = y_0
    for i in range(N - 1):
        k1 = f(ts[i], ys[i])
        k2 = f(ts[i] + tau, ys[i] + tau * k1)
        k3 = f(ts[i] + tau/2, ys[i] + tau/2 * (k1 + k2)/2 )
        ys[i + 1] = ys[i] + tau/6 * (k1 + k2 + 4*k3)
    return ts, ys

def rk4(f, t_0, y_0, tau, N):
    ts = np.linspace(t_0, t_0 + (N - 1) * tau, N)
    ys = np.zeros(N)
    ys[0] = y_0
    for i in range(N - 1):
        k1 = f(ts[i], ys[i])
        k2 = f(ts[i] + tau/2, ys[i] + tau/2 * k1)
        k3 = f(ts[i] + tau/2, ys[i] + tau/2 * k2)
        k4 = f(ts[i] + tau, ys[i] + tau * k3)
        ys[i + 1] = ys[i] + tau/6 * (k1 + 2*k2 + 2*k3 + k4)
    return ts, ys