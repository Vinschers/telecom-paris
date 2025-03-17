import numpy as np
from skimage import io
import matplotlib.pyplot as plt


def plot(img: np.ndarray):
    plt.imshow(img, cmap="gray")
    plt.show()


def gradient_descent(grad, x_shape, x_init=None, tau=0.1, max_iter=1000) -> np.ndarray:
    if x_init is None:
        x_init = np.random.rand(*x_shape)

    iters = 0
    x = x_init

    while iters < max_iter:
        x = x - tau * grad(x)
        iters += 1

    return x


def tychonov(img: np.ndarray, param_lambda: float = 1):
    def grad(u):
        d2x = np.zeros_like(u)
        d2y = np.zeros_like(u)

        d2x[1:-1, 1:-1] = u[1:-1, :-2] - 2 * u[1:-1, 1:-1] + u[1:-1, 2:]
        d2y[1:-1, 1:-1] = u[:-2, 1:-1] - 2 * u[1:-1, 1:-1] + u[2:, 1:-1]

        jacobian = d2x + d2y

        return u - img - 2 * param_lambda * jacobian

    return gradient_descent(grad, img.shape)


def total_variation(img: np.ndarray, param_lambda: float = 1, epsilon: float = 0.01):
    def grad(u):
        dx = np.gradient(u, axis=1)
        dy = np.gradient(u, axis=0)

        mag_grad_u = np.sum(np.square(np.abs(dx))) + np.sum(np.square(np.abs(dy)))

        grad_tv = (np.square(dx) + np.square(dy)) / np.sqrt(np.square(epsilon) + mag_grad_u)

        return u - img - grad_tv

    return gradient_descent(grad, img.shape)


if __name__ == "__main__":
    img = io.imread("images/pyrabruit.tif", as_gray=True)
    img = img.astype(np.float32)

    plot(tychonov(img))
    # plot(total_variation(img, 10, 0.1))
