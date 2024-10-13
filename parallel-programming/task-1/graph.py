# %%

import matplotlib.pyplot as plt
import numpy as np

def S(alpha, beta, p):
  return 1 / (alpha + beta / p)

# processors
ps = np.array([1, 2, 4])
t_alpha = np.average([4.45, 4.47, 4.51])

t_beta = np.array([
  [15.04, 15.15, 15.39],
  [8.47, 8.81, 8.31],
  [4.16, 4.16, 4.24]
])

t_beta = np.average(t_beta, axis=1)

alpha = t_alpha / (t_alpha + t_beta[0])
beta = t_beta[0] / (t_alpha + t_beta[0])

linear = ps
theoretical_speedup = S(alpha, beta, ps)
measured_beta_speedup = t_beta[0]/t_beta
measured_speedup = (t_alpha + t_beta[0])/(t_alpha + t_beta)

plt.xticks(ps)
plt.xlabel('procesoriai $(p)$')
plt.ylabel('pagreitėjimas')
plt.plot(ps, linear, linestyle='dashed', label=f'$f(p)=p$')
plt.plot(ps, theoretical_speedup, linestyle='dashed', label='$\\tilde{S}_p$')
plt.plot(ps, measured_beta_speedup, marker='.', label='$\\frac{t_{\\beta}(1)}{t_{\\beta}(p)}$')
plt.plot(ps, measured_speedup, marker='.', label='$\\frac{t(1)}{t(p)}$')
plt.legend()
plt.show()

# %%
