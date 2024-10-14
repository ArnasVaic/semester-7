# %%

import matplotlib.pyplot as plt
import numpy as np

# processors
ps = np.array([1, 2, 4])

t_1 = np.average([
  [4.2897, 4.05183, 4.07159],
  [1.90986, 2.04499, 2.1479],
  [1.03414, 1.0053, 1.03196]
], axis=1)

t_2 = np.average([
  [14.7818, 15.2255, 14.4146],
  [6.27518, 6.54402, 8.04437],
  [3.83722, 3.78994, 3.76172]
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
