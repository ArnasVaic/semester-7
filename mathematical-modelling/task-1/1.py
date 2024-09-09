# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc
import inspect

np.seterr(divide="ignore")

# %%
def cauchy_problem(F, x0, y0, x, y_min, y_max):

    if(x0 < x[0] or x0 > x[-1]):
        raise Exception("Initial point must be within given x value range")

    N = x.size - 1 
    N0 = round(N * (x0 - x[0]) / (x[-1] - x[0]))

    #print("x size = ", x.size)
    #print("N0 = ", N0)
    #print("y_min = ", y_min, "y_max = ", y_max)

    x = x + (x0 - x[N0])

    # points that were calculated by numerically integrating 
    # in the positive direction of given x values from the initial point p
    positive_points = []
    
    prev_y = y0

    for point in zip(x[N0:], sc.odeint(F, y0, x[N0:]).flatten()):
        
        # if y values go beyond some point, stop plotting
        point_y = point[1]

        if(abs(prev_y - point_y) > 400 / N):
            break

        prev_y = point_y

        positive_points.append(point)

        if(point_y < y_min or point_y > y_max or np.isnan(point_y)):
            break

    prev_y = y0

    # points that were calculated by numerically integrating 
    # in the negative direction of given x values from the initial point p
    negative_points = []
    for point in list(zip(x[N0::-1], sc.odeint(F, y0, x[N0::-1]).flatten())):

        # if y values go beyond some point, stop plotting
        point_y = point[1]

        if(abs(prev_y - point_y) > 400 / N):
            break

        prev_y = point_y
        
        negative_points.append(point)

        if(point_y < y_min or point_y > y_max or np.isnan(point_y)):
            break

    negative_points.reverse()
    zipped = negative_points + positive_points
    unzipped = list(zip(*zipped))

    xs, ys = unzipped

    return (xs, ys)

# %%
def visualize(
        model, 
        analytical_solution, 
        bounds = [(-1,1), (-1,1)], 
        slope_field_samples=30, 
        sol_samples=1000, p = (-0.5,-0.5)):
    X = np.linspace(bounds[0][0], bounds[0][1], slope_field_samples)
    Y = np.linspace(bounds[1][0], bounds[1][1], slope_field_samples)

    XS, YS = np.meshgrid(X, Y)

    FY = model(XS, YS)
    
    FX = 1 / np.sqrt(1 + FY**2)
    FY = FX * FY

    XP = np.linspace(bounds[0][0], bounds[0][1], sol_samples)
    p1 = cauchy_problem(lambda y, x: model(x, y), *p, XP, bounds[1][0], bounds[1][1])

    XP = np.linspace(bounds[0][0], bounds[0][1], sol_samples)

    print(XP.shape)

    # in this case analytics solutions returns two branches
    p2ys1, p2ys2 = analytical_solution(XP)

    plt.figure(figsize = (6,6))
    
    plt.quiver(XS, YS, FX, FY, color="red", pivot="mid", headaxislength=0, headwidth=0, headlength=0);
    plt.quiver(XS, YS, -FY, FX, color="blue", pivot="mid", headaxislength=0, headwidth=0, headlength=0);

    plt.plot(*p1, color="red")
    plt.plot(XP, p2ys1, color="blue")
    plt.plot(XP, p2ys2, color="blue")

    margin = 0.1
    plt.xlim([bounds[0][0] - margin, bounds[0][1] + margin])
    plt.ylim([bounds[1][0] - margin, bounds[1][1] + margin])

    plt.show()

# %%

C = 1
def analytical_solution(xs, C):
    solution = np.sqrt(-2 + C * np.exp(-2 * np.arcsin(xs / np.sqrt(5))))
    # we have an expression for y^2 so we need to visualize two branches
    return (-solution, solution)

# First problem expressed in the form F(x, y) = y'
def F(x, y):
    return -(y ** 2 + 2) / (y * np.sqrt(5 - x ** 2))

visualize(F, lambda x: analytical_solution(x, C), bounds=[(-5, 5), (-5, 5)], p=(-2, 4))
# %%
