import numpy as np

class SimpleNet:

    def train(self, X, max_iter=10000):
        self.syn0 = 2 * np.random.random(X.T.shape) - 1
        self.syn1 = 2 * np.random.random(X.shape) - 1
        for j in xrange(max_iter):
            l1 = 1 / (1 + np.exp(-(np.dot(X, self.syn0))))
            l2 = 1 / (1 + np.exp(-(np.dot(l1, self.syn1))))
            l2_delta = (X - l2) * (l2 * (1 - l2))
            l1_delta = l2_delta.dot(self.syn1.T) * (l1 * (1 - l1))
            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += X.T.dot(l1_delta)
            print("step {0}".format(j))

    def predict(self, X):
        l1 = 1 / (1 + np.exp(-(np.dot(X, self.syn0))))
        l2 = 1 / (1 + np.exp(-(np.dot(l1, self.syn1))))
        return l2

# X = y in here

X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
y = np.array([[0,1,1,0]]).T





