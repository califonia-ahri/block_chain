# ECC uses y^2 = x^3 + a*x + b
# In addition operator P(x1, y1) Q(x2, y2) R(x3, y3)
# x3 = s^2 - x1 - x2 mod p
# y3 = s(x1-x3) - y1 mod p
# if P!=Q s = ((y2-y1)/(x2-x1)) mod p
# if P==Q s = ((3x1^2 + a)/2*y1) mod p
# To get inversion a^-1 we use Fermat's little theorem

import math
import numpy as np
import matplotlib.pyplot as plt

# additive Operation
def addOperation(a, b, p, q, m):
    if q == (math.inf, math.inf):
        return q

    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]

    if p == q:
        # Doubling
        # slope (s)
        # get inversion first (a^-1 = a^p-2 mod p)
        r = 2 * y1
        rInv = pow(r, m - 2, m)
        s = (rInv * (3 * (x1**2) + 1)) % m
    else:
        r = x2 - x1
        rInv = pow(r, m - 2, m)  # Fermat's little theorem
        s = (rInv * (y2 - y1)) % m

    x3 = (s**2 - x1 - x2) % m
    y3 = (s * (x1 - x3) - y1) % m
    return x3, y3


# y^2 = x^3 + 2*x + 2 mod 127
a = 2
b = 2
m = 127
P = (5, 1)
Q = P

allPoints = [P]
while 1:
    # check if R is inverse of P, then it is infinity spot
    # if A(x1, y1) B(x2, y2) and x1==x2, y1 and y2 is additive inverse to (mod m)

    if (Q[0] == P[0]) & (abs(Q[1] - m) == P[1]):
        # stop in here
        break
    else:
        # if not keep searching group's elements
        R = addOperation(a, b, P, Q, m)
        allPoints.append(R)
        Q = R

x, y = np.array(allPoints).T
plt.figure(figsize=(8, 6))
plt.scatter(x, y, marker="o", color="green", alpha=0.5, s=150)
plt.show()
print(allPoints)
