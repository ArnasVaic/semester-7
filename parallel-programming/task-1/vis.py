# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

with open('demandPoints.dat') as input:
    lines = input.readlines()
    tokenized = [ line.strip().split('\t') for line in lines ]
    xs = np.array([ float(tokens[0]) for tokens in tokenized ])
    ys = np.array([ float(tokens[1]) for tokens in tokenized ])
    ps = np.array([ float(tokens[2]) for tokens in tokenized ])

    colors = cm.rainbow(np.linspace(0, 1, np.max(ps)))

    for x, y, c in zip(xs, ys, colors):
        plt.scatter(x, y, color=c)

# %%
