import numpy as np
from copy import deepcopy

from utils import diff, abs


def gradient_descent(F, grad_F, x_shape, x_init, tau=0.01, delta=1e-5, max_iter=1_000):
    print(f"{tau = }")

    if x_init is None:
        x = np.random.rand(*x_shape)
    else:
        x = deepcopy(x_init)

    base_f = F(x)
    F_values = []
    iters = 0

    while iters < max_iter:
        delta_x = tau * (-grad_F(x))

        x += delta_x

        F_values.append(F(x) / base_f)

        if (abs(delta_x)).max() < delta:
            break

        iters += 1
    return x, F_values
