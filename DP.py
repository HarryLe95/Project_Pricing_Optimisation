from __future__ import annotations

from typing import Optional, Any

import numpy as np


class Table:
    def __init__(self, N: int, M: int):
        self.N = N
        self.M = M
        self.prices = np.linspace(0, 1, self.M)
        self.data = np.zeros((N + 1, N + 1, M))
        self.data[:, 0, 0] = np.arange(N + 1)
        self.best_prices = np.zeros((N + 1, N + 1, M))

    def get_index(self, price: float) -> int:
        diff = np.abs(self.prices - price)
        return np.argmin(diff)

    def get_price(self, i: int, j: int, p: float) -> float:
        k = self.get_index(p)
        return self.best_prices[i, j, k]

    def set_price(self, i: int, j: int, p: float, value: float):
        k = self.get_index(p)
        self.best_prices[i, j, k] = value

    def __getitem__(self, index: tuple[int, int, float]) -> float:
        i = index[0]
        j = index[1]
        p = index[2]
        k = self.get_index(p)
        return self.data[i, j, k]

    def __setitem__(self, index: tuple[int, int, float], value: float):
        i = index[0]
        j = index[1]
        p = index[2]
        k = self.get_index(p)
        self.data[i, j, k] = value

    def create_node(self, i: int, j: int, p: float):
        best_price = self.get_price(i, j, p)
        if j >= 1:
            accept = self.create_node(i + 1, j - 1, p - best_price)
            reject = self.create_node(i, j - 1, p)
        else:
            accept = None
            reject = None
        return Policy(best_price, accept, reject)

    def build(self):
        return self.create_node(0, self.N, 1)


class Policy:
    def __init__(
        self, value: float, accept: Optional[Policy], reject: Optional[Policy]
    ):
        self.value = value
        self.accept = accept
        self.reject = reject

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)


def get_dp_strategy(N: int, M: int) -> dict[str, Any]:
    T = Table(N, M)

    for j in range(1, N):
        for i in range(0, N - j + 1):
            for p in T.prices:
                search_values = [
                    (1 - s) * T[i + 1, j - 1, p - s] + s * T[i, j - 1, p]
                    for s in T.prices
                    if s <= p
                ]
                best_price = T.prices[np.argmax(search_values)]
                T.set_price(i, j, p, best_price)
                T[i, j, p] = np.max(search_values)
    search_values = [
        (1 - s) * T[1, N - 1, 1 - s] + s * T[0, N - 1, 1] for s in T.prices
    ]
    best_price = T.prices[np.argmax(search_values)]
    T.set_price(0, N, 1, best_price)
    T[0, N, 1] = np.max(search_values)
    price = T.build()
    return {"E": T[0, N, 1], "policy": price, "table": T}


if __name__ == "__main__":
    N = 3
    dp = get_dp_strategy(N, 500)
    print(dp["E"])
