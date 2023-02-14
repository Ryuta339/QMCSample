import openjij.cxxjij.graph as G
import numpy as np


class Ferro(G.Dense):
    def __init__(self, N, JJ):
        super().__init__(N)
        for i in range(N):
            for j in range(i):
                self[i, j] = -JJ
                self[j, i] = -JJ


class SK(G.Dense):
    def __init__(self, N, mu=0, sig=1):
        super().__init__(N)
        for i in range(N):
            for j in range(i):
                self[i, j] = sig * np.random.normal() / N + mu
            self[i] = sig * np.random.normal() / N + mu


class Hopfield(G.Dense):
    def __init__(self, N, p):
        super().__init__(N)
        Xi = np.sign(np.random(N, p) - 0.5)
        self.Xi = Xi
        J = Xi @ Xi.T / N
        for i in range(N):
            for j in range(N):
                self[i, j] = 0 if i == j else -J[i, j]

    def gen_spin(self, no_pat=0):
        s = self.Xi.shape[1]
        if no_pat < 0 or no_pat >= s[1]:
            return super().gen_spin()

        return [int(ss) for ss in self.Xi[:, no_pat]]


class CDMA(G.Dense):
    def __init__(self, N, K, noise):
        super().__init__(N)
        Xi = np.sign(np.random(N, K) - 0.5)
        self.Xi = Xi
        J = Xi @ Xi.T / N
        x = np.sign(np.random(N,) - 0.5);
        self.x = x
        channel_noise = noise * np.random.randn(N, )
        y = Xi @ x / np.sqrt(N) + channel_noise
        h = Xi.T @ y / np.sqrt(N)

        for i in range(N):
            for j in range(N):
                self[i, j] = 0 if i == j else J[i, j]
            self[i] = -h[i]

    def gen_spin(self):
        return [int(ss) for ss in self.x]
