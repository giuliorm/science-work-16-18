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

    def solve_diff(self, t):
        # Solve diff and returns a
        # y is an initial condition of y
        initial = np.array([random.random() * 2 * 0.6 - 0.6 for i in range(0, len(self.w))])
        sol = odeint(func=self.__diff_func, y0=initial, t=t)
        #self.plot_diff(t, sol, range(1, len(self.w)))
        self.a = sol
        # Return vector solution
        return sol


    def newNet(self, X, y, linspace, alpha=0.2, eps=10e-4):
        for x in range(200):
            for i in xrange(self.w.shape[0]):
                for j in xrange(self.w.shape[1]):
                    oldW = self.w[i][j]
                    self.w[i][j] += eps
                    preds1 = self.solution(y, linspace)
                    error1 = preds1 - y
                    gradient1 = X.T.dot(error1) / X.shape[0] # ??????
                    self.w[i][j] = oldW
                    self.w[i][j] -= eps
                    preds2 = self.solution(y, linspace)
                    error2 = preds2 - y
                    gradient2 = X.T.dot(error2) / X.shape[0]  # ??????
                    loss =  [np.sum(np.sum(error1[:,k])- np.sum(error2[:,k]))/2
                             for k in range(error1.shape[1])]
                    print "[INFO] epoch #{0}, weight #{1}#{2} loss={{".format(x + 1, i, j),
                    for l in loss:
                        print " {0},".format(l),
                    print("}")
                    gradient = (gradient1 - gradient2)/(2*eps)
                    self.w[i][j] = oldW
                    self.w += alpha * gradient

    def __cost(self, y, linspace):
        y = np.asarray(y)
        diff = self.solution(y, linspace) - y
        return 0.5 * np.mean(diff ** 2)

    def __grad__(self, y, linspace, eps = 0.01):
        # w_0 = self.w
        num_grad = np.zeros(self.w.shape)
        # initial_cost = J(neuron, X, y)

        for i in range(self.w.shape[0]):
            old_wi = self.w[:,i].copy()
            # change weight

            self.w[:,i] += eps
            gradPlus = self.__cost(y, linspace)

            self.w[:,i] = old_wi

            self.w[:,i] -= eps
            gradMinus = self.__cost(y, linspace)

            # New value of J and new value of grad with i-th weight
            num_grad[i] = (gradPlus - gradMinus)/(2*eps)

            # get weights back
            self.w[:,i] = old_wi

        return num_grad

    def solution(self, y, linspace):
        solution = []
        diffSol = self.solve_diff(linspace)
        return np.asarray(diffSol)

    def generate(self, y, linspace):
        return self.solution(y, linspace)

    def fit(self, y, batch_size, linspace, learning_rate=0.1, eps=1e-6, max_steps=100):
        indexes = list(range(len(y)))
        for i in range(1, max_steps):
            # iteration tracking
            self.time = i
            sample_ind = 0
            max = 200
            if len(y) != batch_size:
                while max >= 0:
                    sample_ind, = np.random.choice(a=indexes, size=1, replace=False)
                    begin = sample_ind - batch_size
                    end = sample_ind + batch_size
                    if (begin >= 0 or end <= len(y)):
                        break
                    max = max - 1
            begin = sample_ind - batch_size
            end = sample_ind + batch_size
            if begin >= 0:
                batchY = y[sample_ind - batch_size:sample_ind]
                batchT = linspace[sample_ind - batch_size:sample_ind]
            elif end < len(y):
                batchY = y[sample_ind:sample_ind + batch_size]
                batchT = linspace[sample_ind:sample_ind + batch_size]
            else:
                batchY = y[:]
                batchT = linspace[:]
            rez = self.__update_mini_batch(batchY, batchT, learning_rate, eps)
            print("step " + str(i))
            if rez:
                return 1

        return 0
# comment
    def __update_mini_batch(self, y, linspace, learning_rate, eps):
        #for yitem in y:
        grad = self.__grad__(y, linspace)

        jBefore = self.__cost(y, linspace)
        self.w = self.w - learning_rate * grad
        jAfter = self.__cost(y, linspace)

        rez = 1 if abs(jBefore - jAfter) <= eps else 0

        return rez

from math import cos
from math import sin
from math import pow
from math import e
# neuron count corresponds to number of joints

n = NeuralNetwork(neurons_count=2)
# sol = n.solve_diff(np.asarray([cos(x) for x in range(-10, 10)]))
data = []

t = np.linspace(-5, 5, 1000)

#for i in range(len(t)):
#    data.append([t[i], -0.25 * omega - 5.0 * np.sin(theta)])

def pend(y, t):
    theta, omega = y
    dydt = [omega, -0.25 * omega - 5.0 * np.sin(theta)]
    return dydt

sol = odeint(func=pend, y0=[np.pi - 0.1, 0.0], t=t)
#n.plot_diff(t, sol, ["theta ", "omega"])
n.newNet(sol, sol, t)
genData = n.generate(sol[:,0], t)
n.plot_diff(t, genData, ["theta ", "omega"])
while(True):
    pass
rez = n.fit(y=sol[:,0], batch_size=1000, linspace=t)
genData = np.asarray([[x] for x in n.generate(sol[:,0], t)])
n.plot_diff(t, genData, ["theta "])

print("Network train result: ")
print(rez)


#
#i = 1