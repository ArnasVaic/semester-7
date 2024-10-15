# %%

import matplotlib.pyplot as plt
import numpy as np

# processors
ps = np.array([1, 2, 4])

t_1 = np.average([
  [3.74426, 4.5179, 4.48975],
  [2.07918, 1.9611, 2.03437],
  [1.22207, 1.16934, 1.14002]
], axis=1)

t_2 = np.average([
  [19.3091, 21.1846, 19.3564],
  [9.96903, 9.79868, 10.0692],
  [5.86876, 5.58835, 5.13483]
], axis=1)

linear = ps
measured_t1_speedup = t_1[0] / t_1
measured_t2_speedup = t_2[0] / t_2
measured_t_speedup = (t_1[0] + t_2[0]) / (t_1 + t_2)

plt.xticks(ps)
plt.xlabel('procesoriai $(p)$')
plt.ylabel('pagreitėjimas')
plt.plot(ps, linear, linestyle='dashed', label='$f(p)=p$')
plt.plot(ps, measured_t1_speedup, marker='.', label='$\\frac{t_1(1)}{t_1(p)}$')
plt.plot(ps, measured_t2_speedup, marker='.', label='$\\frac{t_2(1)}{t_2(p)}$')
plt.plot(ps, measured_t_speedup, marker='.', label='$\\frac{t(1)}{t(p)}$')
plt.legend()
plt.show()

# %%
