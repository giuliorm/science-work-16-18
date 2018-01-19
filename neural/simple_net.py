import numpy as np
from scipy.integrate import odeint
import random
class SimpleNet:

    def __init__(self, neurons_count=3, eps=10e-6):
        self.w = np.array([np.array([random.random() * 2 * eps - eps for i in range(0, neurons_count)])
                           for i in range(0, neurons_count)])

    def __diff_func(self, y, t):
        dydt = []
        for i in range(0, len(y)):
            e_i = 0
            for j in range(0, len(y)):
                e_i = e_i + y[j] * self.w[i][j]
            dydt.append(e_i)
        return dydt

    def solve_diff(self, t):
        # Solve diff and returns a
        # y is an initial condition of y
        initial = np.array([random.random() * 2 * 0.6 - 0.6 for i in range(0, len(self.w))])
        sol = odeint(func=self.__diff_func, y0=initial, t=t)
        #self.plot_diff(t, sol, range(1, len(self.w)))
        self.a = sol
        # Return vector solution
        return sol

    def train(self, t, X, max_iter=10000):
        #self.syn0 = 2 * np.random.random(X.T.shape) - 1
        #self.syn1 = 2 * np.random.random(X.shape) - 1
        for j in xrange(max_iter):
            l = self.solve_diff(t)
            for x in xrange(l.shape[1]):
                l_delta = (X - l) ** self.__diff_func(l[:,x], t)
            #l1 = 1 / (1 + np.exp(-(np.dot(X, self.syn0))))
            #l2 = 1 / (1 + np.exp(-(np.dot(l1, self.syn1))))
            #l2_delta = (X - l2) * (l2 * (1 - l2))
            #l1_delta = l2_delta.dot(self.syn1.T) * (l1 * (1 - l1))
            #self.syn1 += l1.T.dot(l2_delta)
                self.w += X.T.dot(l1_delta)
            l1 = self.solve_diff(t)
            print("step {0}".format(j))

# X = y in here

X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
y = np.array([[0,1,1,0]]).T
t = np.linspace(-5, 5, 1000)




