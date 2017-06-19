__author__ = 'JuriaSan'
import numpy as np
import random
from scipy.integrate import odeint
import matplotlib.pyplot as plt
class NeuralNetwork:

    neurons_count = 0
    time = 0

    #TODO: define a proper range of ode solution

    def __init__(self, neurons_count, eps=10e-2):

        # Randomly initialize weights

        self.a = np.array([random.random() * 2 * eps - eps for i in range(0, neurons_count)])
        self.w = np.array([np.array([random.random() * 2 * eps - eps for i in range(0, neurons_count)])
                           for i in range(0, neurons_count)])

        self.neurons_count = neurons_count


    def plot_diff(self, t, sol, labels):
        for i in range(0,len(labels)):
            plt.plot(t, sol[:, i], label=str(labels[i]))

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

    #ya - vector of begin conditions. a(i - 1) in generative mode, and y(i) in learn mode
    def solve_diff(self, y):
        #solve diff and returns a

        t = np.linspace(0, 10, 101)
        sol = odeint(self.__diff_func, y, t)
#       self.plot_diff(t, sol, range(1, len(self.a)))

        #return vector solution
        return np.asarray(sol)

    def __cost(self, y):
        y = np.asarray(y)
        solution = self.solve_diff(y)
        diff = solution - y
        return 0.5 * np.mean(diff ** 2)

    def __grad__(self, y, eps = 0.01, J=__cost):
        #w_0 = self.w
        num_grad = np.zeros(self.w.shape)
        #initial_cost = J(neuron, X, y)

        for i in range(len(self.w)):
            old_wi = self.w[i].copy()
            # change weight

            self.w[i] += eps
            gradPlus = J(y)

            self.w[i] = old_wi

            self.w[i] -= eps
            gradMinus = J(y)

            # New value of J and new value of grad with i-th weight
            num_grad[i] = (gradPlus - gradMinus)/(2*eps)

            # get weights back
            self.w[i] = old_wi

        return num_grad

    def fit(self, y, batch_size, learning_rate=0.1, eps=1e-6, max_steps=200):
        indexes = list(range(len(y)))
        for i in range(1, max_steps):
            #iteration tracking
            self.time = i

            sample_ind = np.random.choice(a=indexes, size=batch_size, replace=False)

            batchY = y[sample_ind]

            rez = self.__update_mini_batch(batchY, learning_rate, eps)
            if rez:
                return 1

        return 0

    def __update_mini_batch(self, y, learning_rate, eps):

        grad = self.__grad__(y)

        jBefore = self.__cost(y)
        self.w = self.w - learning_rate * grad
        jAfter = self.__cost(y)

        rez = 1 if abs(jBefore - jAfter) <= eps else 0
        return rez

from math import cos

n = NeuralNetwork(neurons_count=1)
sol = n.solve_diff(np.asarray([cos(x) for x in range(-10, 10)]))
