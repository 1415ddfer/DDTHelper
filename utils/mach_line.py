import math

import numpy as np
from scipy.optimize import fsolve


def _calF(angel, wind, dx, dy):
    R, W, g = [0.89927083, 5.8709153, -172.06527992]
    angel = angel * math.pi / 180

    def solve(F):
        vx = math.cos(angel) * F
        vy = math.sin(angel) * F

        def computePosition(v0, f, R, t):
            temp = f - R * v0
            ert = np.power(math.e, -R * t)
            right = temp * ert + f * R * t - temp
            return right / (R * R)

        def getTime(v0):
            solve_l = lambda t: computePosition(v0, g, R, t) - dy
            time = fsolve(solve_l, [100000])
            assert time[0] != 0
            return time[0]

        t = getTime(vy)
        return computePosition(vx, W * wind, R, t) - dx

    f = fsolve(solve, [100])
    if f[0] > 100:
        raise ValueError
    return f[0]


if __name__ == '__main__':
    # 角度 风(右正左负) x y
    print(_calF(90, 1.6, 1.5, 5.5))
