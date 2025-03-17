import numpy as np
import torch


"""
We use the roll function to compute the derivatives because we assume that the image is periodic.
"""
def D(img, axis):
    if isinstance(img, np.ndarray):
        return np.roll(img, -1, axis) - img
    return torch.roll(img, -1, axis) - img


def D_transpose(img, axis):
    if isinstance(img, np.ndarray):
        return np.roll(img, 1, axis) - img
    return torch.roll(img, 1, axis) - img


def Dx(img):
    return D(img, 1)


def Dy(img):
    return D(img, 0)


def Dx_transpose(img):
    return D_transpose(img, 1)


def Dy_transpose(img):
    return D_transpose(img, 0)


def grad(img):
    if isinstance(img, np.ndarray):
        return np.stack((Dx(img), Dy(img)), axis=0)
    return torch.stack((Dx(img), Dy(img)), dim=0)


"""
The laplacian is $- \nabla^\top (\nabla I)$.
"""
def laplacian(img):
    return -(Dx_transpose(Dx(img)) + Dy_transpose(Dy(img)))
