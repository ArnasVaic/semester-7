# %%

import matplotlib.pyplot as plt
import numpy as np

# processors
ps = np.array([1, 2, 4])

t_1 = np.average([
  [4.67692, 4.71238, 4.75531],
  [2.07918, 1.9611, 2.03437],
  [1.22936, 1.23446, 1.22374]
], axis=1)

t_2 = np.average([
  [25.5489, 23.8423, 23.9163],
  [13.0758, 12.3878, 11.5776],
  [6.27233, 5.94331, 5.55882]
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
