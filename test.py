from numpy import linspace


a = linspace(10.000000, -10.000000, 1000)

b = linspace(-10.000000, 10.000000, 1000)


for i, j in zip(a, b):
    print(i,j)