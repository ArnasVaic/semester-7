# %%
import numpy as np
def x(t):
    return np.sin(t)/2 + np.cos(4*t)/7+np.sin(3*t)/6-np.cos(3*t)/7
ts = np.linspace(0, 2 * np.pi, 1000)
xs = x(ts)
np.min(xs), np.max(xs)
# %%
