__author__ = 'JuriaSan'
import numpy as np
import random
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class NeuralNetwork:


    # TODO: define a proper range of ode solution

    def __init__(self, neurons_count, eps=10e-2):

        # Randomly initialize weights
        self.neurons_count = 0
        self.time = 0
        self.a = np.array([random.random() * 2 * eps - eps for i in range(0, neurons_count)])
        self.w = np.array([np.array([random.random() * 2 * eps - eps for i in range(0, neurons_count)])
                           for i in range(0, neurons_count)])

        self.neurons_count = neurons_count

    def plot_diff(self, t, sol, labels):
        for i in range(0,len(labels)):
            plt.plot(t, sol[i, :], label=str(labels[i]))

        plt.legend(loc='best')
        plt.xlabel('t')
        plt.grid()
        plt.show()

    def __diff_func(self, y, t):
        dydt = []
        for i in range(0, len(y)):
            e_i = 0
            for j in range(0, len(y)):
                e_i = e_i + y[j] * self.w[i][j]
            dydt.append(e_i)
        return dydt


    # ya - vector of begin conditions. a(i - 1) in generative mode, and y(i) in learn mode
    def solve_diff(self, y, t):
        # Solve diff and returns a

        sol = odeint(self.__diff_func, y, t)
        self.a = sol
        # self.plot_diff(t, sol, range(1, len(self.a)))

        # Return vector solution
        return self.a

    def __cost(self, y, linspace):
        y = np.asarray(y)
        solution = self.solve_diff(y, linspace)
        diff = solution - y
        return 0.5 * np.mean(diff ** 2)

    def __grad__(self, y, linspace, eps = 0.01):
        # w_0 = self.w
        num_grad = np.zeros(self.w.shape)
        # initial_cost = J(neuron, X, y)

        for i in range(len(self.w)):
            old_wi = self.w[i].copy()
            # change weight

            self.w[i] += eps
            gradPlus = self.__cost(y, linspace)

            self.w[i] = old_wi

            self.w[i] -= eps
            gradMinus = self.__cost(y, linspace)

            # New value of J and new value of grad with i-th weight
            num_grad[i] = (gradPlus - gradMinus)/(2*eps)

            # get weights back
            self.w[i] = old_wi

        return num_grad


    def generate(self, linspace):
        self.a = self.solve_diff(self.a, linspace)
        data = []
        for item in self.a:
            data.extend(item)
        return data

    def fit(self, y, batch_size, linspace, learning_rate=0.1, eps=1e-6, max_steps=200):
        indexes = list(range(len(y)))
        for i in range(1, max_steps):
            # iteration tracking
            self.time = i

            sample_ind = np.random.choice(a=indexes, size=batch_size, replace=False)

            batchY = y[sample_ind]

            rez = self.__update_mini_batch(batchY, linspace, learning_rate, eps)
            if rez:
                return 1

        return 0

    def __update_mini_batch(self, y, linspace, learning_rate, eps):

        grad = self.__grad__(y, linspace)

        jBefore = self.__cost(y, linspace)
        self.w = self.w - learning_rate * grad
        jAfter = self.__cost(y, linspace)

        rez = 1 if abs(jBefore - jAfter) <= eps else 0
        return rez

from math import cos
from math import sin

n = NeuralNetwork(neurons_count=1)
# sol = n.solve_diff(np.asarray([cos(x) for x in range(-10, 10)]))
sinData = []

t = np.linspace(-10, 10, 50)

for i in range(len(t)):
    sinData.append(sin(t[i]))

rez = n.fit(y=np.asarray(sinData), batch_size=1, linspace=t)

print("Network train result: ")
print(rez)


n.plot_diff(t, np.asarray([np.asarray(sinData), np.asarray(genData)]) , ["sinus", "gen"])
i = 1