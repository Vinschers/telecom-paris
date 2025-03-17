from utils import sum, sqrt, squared_norm
from differentiation import Dx, Dy, grad, laplacian


def F_TV(x, v, epsilon, lambda_, func):
    data_fidelity = sum((func(x) - v) ** 2) / 2
    regularization = lambda_ * sum(sqrt(epsilon ** 2 + Dx(x) ** 2 + Dy(x) ** 2))

    return data_fidelity + regularization


def dF_TV(x, v, epsilon, lambda_):
    data_fidelity = x - v
    regularization = - lambda_ * laplacian(x) / sqrt(epsilon ** 2 + squared_norm(grad(x)))

    return data_fidelity + regularization


"""
This is the generator function. Based on the parameters specified, it returns the total variation error function that has only one input, which is then used in the gradient descent algorithm
"""
def total_variation(img, epsilon, lambda_, func):
    def F(x):
        return F_TV(x, img, epsilon, lambda_, func)

    def dF(x):
        return dF_TV(x, img, epsilon, lambda_)

    L = 1 + (8 * lambda_) / epsilon
    tau = 1.9 / L
    return F, dF, tau
