import torch

from utils import diff


def gradient_descent(F, expected, x0, tau=2e-2, delta=1e-5, max_iter=100):
    x = x0.clone().requires_grad_(True)
    print(f"{tau = }")
    optim = torch.optim.SGD([x], lr=tau)

    base_f = F(x0).item()
    y = []
    diffs = []
    iters = 0

    while iters < max_iter:
        optim.zero_grad()

        x_prev = x.clone()

        loss = F(x)

        y.append(loss.item() / base_f)
        diffs.append(diff(x, expected))

        loss.backward()
        optim.step()

        if diff(x_prev, x) < delta:
            break

        iters += 1

    return x.detach(), y, diffs
