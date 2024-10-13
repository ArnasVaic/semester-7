# %%

import matplotlib.pyplot as plt
import numpy as np

def S(alpha, beta, p):
  return 1 / (alpha + beta / p)

ps = np.array([1, 2, 4])
t_1 = np.average([
  5.06828,
  5.29663,
  4.43938
])

t_2 = np.average([
  [15.8976, 15.1475, 16.6864],
  [8.21124, 7.61354, 7.22827],
  [4.15409, 3.86757, 4.30398]
], axis=1)

alpha = t_1 / (t_1 + t_2[0])
beta = t_2[0] / (t_1 + t_2[0])

linear = ps
theoretical_speedup = S(alpha, beta, ps)
measured_beta_speedup = t_2[0]/t_2
measured_speedup = (t_1 + t_2[0])/(t_1 + t_2)

plt.xticks(ps)
plt.xlabel('procesoriai $(p)$')
plt.ylabel('pagreitėjimas')
plt.plot(ps, linear, linestyle='dashed', label=f'$f(p)=p$')
plt.plot(ps, theoretical_speedup, linestyle='dashed', label='$\\tilde{S}_p$')
plt.plot(ps, measured_beta_speedup, marker='.', label='$\\frac{t_2(1)}{t_2(p)}$')
plt.plot(ps, measured_speedup, marker='.', label='$\\frac{t(1)}{t(p)}$')
plt.legend()
plt.show()

# %%
