import numpy as np
import torch


"""
This file contains many common functions used in the project.
They were implemented in such a way that they can be used with both numpy arrays and torch tensors.
"""


def sum(x):
    if isinstance(x, np.ndarray):
        return np.sum(x)
    return torch.sum(x)


def sqrt(x):
    if isinstance(x, torch.Tensor):
        return torch.sqrt(x)
    return np.sqrt(x)


def abs(x):
    if isinstance(x, np.ndarray):
        return np.abs(x)
    return torch.abs(x)


def sin(x):
    if isinstance(x, np.ndarray):
        return np.sin(x)
    return torch.sin(x)


def squared_norm(x):
    return sum(x ** 2)


def log10(x):
    if isinstance(x, np.ndarray):
        return np.log10(x)
    return torch.log10(x)


def clip(x, a, b):
    if isinstance(x, np.ndarray):
        return np.clip(x, a, b)
    return torch.clip(x, a, b)


def fft(img):
    if isinstance(img, np.ndarray):
        return np.fft.fft2(img, axes=(0, 1)) # The axes (or dim) parameter is important: it ensures that the FFT is computed in each color channel.
    return torch.fft.fft2(img, dim=(0, 1))


def ifft(img):
    if isinstance(img, np.ndarray):
        return np.fft.ifft2(img, axes=(0, 1)).real
    return torch.fft.ifft2(img, dim=(0, 1)).real


def convolve(img, fft_kernel):
    img = ifft(fft(img) * fft_kernel)
    return img


def normalize(img):
    return (img - img.min()) / (img.max() - img.min())


def diff(img1, img2):
    d = (abs(img1 - img2)).max()

    if isinstance(d, torch.Tensor):
        return d.item()
    return d


def RMSE(img1, img2):
    M, N = img1.shape[:2]
    rmse = sum((img1 - img2) ** 2) / (M * N)
    return sqrt(rmse)


def PSNR(u, v):
    psnr = 20 * log10(u.max() / RMSE(u, v))

    if isinstance(psnr, torch.Tensor):
        return psnr.item()
    return psnr


"""
This function adds dimensions to a torch tensor or numpy array.
This is done in order to use broadcast capabilities correctly throughtout our code.
"""
def add_dims(x, dims):
    for _ in range(dims):
        if isinstance(x, np.ndarray):
            x = np.expand_dims(x, axis=-1)
        else:
            x = x.unsqueeze(-1)

    return x
