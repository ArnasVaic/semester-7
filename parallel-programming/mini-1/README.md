# Minitask 1

## Execution time

| Total time | Reps  |  Average |
| :--------- | :---: | -------: |
| 6s 767ms   |   3   | 2s 255ms |

## $\alpha$, $\beta$ evaluation

$r$ - ratio of average execution time for rand compared to a swap 

from local experiment:

$r = \frac{113}{84} \approx 1.345$

### Theoretical approach

Matrix of size $N \times M$ ($N$ rows and $M$ columns) generates iterates through all matrix cells calling rand so time taken is proportional to $rNM$, for row sorting the bubble-sort algorithm is used to time taken is proportional to $NM^2$. So we have

$$
t_{gen}=rNM\\
t_{sort}=NM^2 
$$

with initial parameters($N=128000, M=200$) we can calculate $\alpha$ and $\beta$:

$$
\alpha=\frac{t_{gen}}{t_{gen}+t_{sort}}=\frac{rNM}{rNM+NM^2}=\frac{rN}{rN+NM}\approx 0.0067\\
\beta=\frac{t_{sort}}{t_{gen}+t_{sort}}=\frac{nM^2}{rNM+NM^2}=\frac{NM}{rN+NM}\approx 0.993
$$

with two times bigger $M$, the results would still be:

$$
\alpha\approx 0.003\\
\beta\approx 0.996
$$

### Practical test

|          | $M=200$ | $M=400$ |
| :------- | :-----: | ------: |
| $\alpha$ |  0.216  |   0.125 |
| $\beta$  |  0.783  |   0.874 |
