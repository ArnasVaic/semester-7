# %%

import matplotlib.pyplot as plt
import numpy as np

def S(alpha, beta, p):
  return 1 / (alpha + beta / p)

ps = np.array([1, 2, 4])
t_1 = np.average([
  4.67692, 
  4.71238, 
  4.75531
])

t_2 = np.average([
  [25.5489, 23.8423, 23.9163],
  [12.6375, 12.0972, 11.6558],
  [6.12905, 6.32013, 6.28199]
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
