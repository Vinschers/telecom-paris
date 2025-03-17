import numpy as np
import torch

from utils import sin, sum, squared_norm, fft, ifft, add_dims
from differentiation import grad, laplacian


"""
Function L used in the analytical solution.
In our implementation, this returns a matrix that is later broadcasted to yield the solution.
"""
def L(v):
    N, M = v.shape[:2]

    if isinstance(v, np.ndarray):
        xi = np.pi * np.arange(N)
        zeta = np.pi * np.arange(M)
    else:
        xi = torch.pi * torch.arange(N, device=v.device)
        zeta = torch.pi * torch.arange(M, device=v.device)

    X = sin(xi / M) ** 2
    Y = sin(zeta / N) ** 2

    return 4 * (X.reshape(N, 1) + Y.reshape(1, M))


"""
Analyticial solution in the Fourier domain.
"""
def u_chapeau(v, lambda_):
    L_matrix = 1 + 2 * lambda_ * L(v)
    L_matrix = add_dims(L_matrix, len(v.shape[2:]))

    return v / L_matrix


"""
Computes the analytical solution.
"""
def analytical_tychonov(img, lambda_):
    img_fft = fft(img)
    u = u_chapeau(img_fft, lambda_)
    return ifft(u)


"""
The following functions are used in the gradient descent algorithm (numerical implementation).
"""

def F_tychonov(x, v, lambda_, func):
    data_fidelity = sum((func(x) - v) ** 2) / 2
    regularization = lambda_ * squared_norm(grad(x))

    return data_fidelity + regularization


def dF_tychonov(x, v, lambda_):
    data_fidelity = x - v
    regularization = - 2 * lambda_ * laplacian(x)

    return data_fidelity + regularization


"""
This is the generator function. Based on the parameters specified, it returns the tychonov error function that has only one input, which is then used in the gradient descent algorithm
"""
def tychonov(img, lambda_, func):
    def F(x):
        return F_tychonov(x, img, lambda_, func)

    def dF(x):
        return dF_tychonov(x, img, lambda_)

    L = 1 + 16 / lambda_
    tau = 1.9 / L
    return F, dF, tau
