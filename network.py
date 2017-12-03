__author__ = 'JuriaSan'
import numpy as np
import random
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from math import e


class NeuralNetwork:

    # TODO: define a proper range of ode solution

    def __init__(self, inputs_count, outputs_count, eps=10e-2):

        # Randomly initialize weights
        #self.neurons_count = 0
        #self.time = 0
        self.l1 = np.array([random.random() * 2 * eps - eps for i in range(0, inputs_count)])
        self.l2 =  np.array([random.random() * 2 * eps - eps for i in range(0, outputs_count)])
        self.w1 = np.array([random.random() * 2 * eps - eps for i in range(0, inputs_count)])
        self.w2 = np.array([random.random() * 2 * eps - eps for i in range(0, outputs_count)])

        self.inputs_count = inputs_count
        self.outputs_count = outputs_count

    def __step(self, w, b):
        return -b/w

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


    # ya - vector of begin conditions. a(i - 1) in generative mode, and y(i) in learn mode

    def solve_diff(self, y, t):
        # Solve diff and returns a

        sol = odeint(self.__diff_func, y, t)
        self.a = sol
        # self.plot_diff(t, sol, range(1, len(self.a)))

        # Return vector solution
        return sol

    def sum(self, w, a):
        s = 0
        for i in range(len(w)):
            s = s + w[i]*a[i]
        return s

    def sigmoid(self, x):
        return 1/(1 + pow(e, -x))

    def l1(self, x):
        l1 = []
        for i in range(len(self.w1)):
            l1.append(self.sigmoid(self.w1[i] * x[i]))
        return l1

    def solution(self, x):

        self.l2 = []
        #for i in range(len(self.w2)):
        #    self.l2.append(self.sigmoid(self.w2[i] * ))

    def __cost(self, y, linspace):
        y = np.asarray(y)
        #solution = self.solve_diff(y, linspace)
        #self.l1 = self.sigmoid(self.sum(self.w1, self.a))
        #self.l2 = self.sigmoid(self.sum(self.w2, self.l1))
        #diff = solution - y
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
        self.solve_diff(self.a[0], linspace)
        data = []
        for item in self.a:
            data.append(item)
        return np.asarray(data)

    def fit(self, y, batch_size, linspace, learning_rate=0.1, eps=1e-6, max_steps=200):
        indexes = list(range(len(y)))
        for i in range(1, max_steps):
            # iteration tracking
            self.time = i

            sample_ind = np.random.choice(a=indexes, size=batch_size, replace=False)

            batchY = y[sample_ind]

            rez = self.__update_mini_batch(batchY, linspace, learning_rate, eps)
            print("step " + str(i))
            if rez:
                return 1

        return 0
# comment
    def __update_mini_batch(self, y, linspace, learning_rate, eps):
        for yitem in y:
            grad = self.__grad__(yitem, linspace)

            jBefore = self.__cost(yitem, linspace)
            self.w = self.w - learning_rate * grad
            jAfter = self.__cost(yitem, linspace)

        rez = 1 if abs(jBefore - jAfter) <= eps else 0

        return rez

from math import cos
from math import sin

# neuron count corresponds to number of joints

n = NeuralNetwork(neurons_count=2)
# sol = n.solve_diff(np.asarray([cos(x) for x in range(-10, 10)]))
sinData = []

t = np.linspace(-30, 30, 10000)

def pend(y, t):
    theta, omega = y
    dydt = [omega, -0.25 * omega - 5.0 * np.sin(theta)]
    return dydt

sol = odeint(func=pend, y0=[np.pi - 0.1, 0.0], t=t)

#for i in range(len(t)):
#    sinData.append([sin(t[i]), cos(t[i])])

rez = n.fit(y=sol, batch_size=20, linspace=t)
#genData = n.generate(t)

n.plot_diff(t, n.a, ["gen sin {0}".format(0)])

print("Network train result: ")
print(rez)


#
#i = 1