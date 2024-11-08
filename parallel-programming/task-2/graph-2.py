# %%

import matplotlib.pyplot as plt
import numpy as np

# processors
ps = np.array([2, 4, 8])

t_1 = np.average([
  [2.21412, 2.50074, 2.15432],
  [1.22579, 1.33768, 1.26524],
  [0.782615, 0.773603, 0.680574]
], axis=1)

t_2 = np.average([
  [15.1587, 14.5044, 13.2824],
  [9.84298, 10.1548, 10.0305],
  [6.67525, 6.60875, 6.94009]
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
