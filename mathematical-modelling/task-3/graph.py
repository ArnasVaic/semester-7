# %%
import numpy as np
import matplotlib.pyplot as plt
def x(t):
    return np.sin(t)/2 + np.cos(4*t)/7+np.sin(3*t)/6-np.cos(3*t)/7
ts = np.linspace(0, 2 * np.pi, 100)
title ="""Lygties $x''+9x=4\sin t-\cos 4t$ Koši sprendinys
su pradinėmis sąlygomis $x(0)=0, x'(0)=1$"""
plt.title(title)
plt.plot(ts, x(ts), label='x(t)')
plt.xlabel('$t$')
plt.ylabel('$x(t)$')
plt.legend()
# %%
