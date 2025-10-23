from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np

class CustomLinearRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations

    def fit(self, X, y):
        self.n_samples, self.n_features = X.shape
        self.weights = np.zeros(self.n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            y_predicted = self.predict(X)
            dw = (1 / self.n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / self.n_samples) * np.sum(y_predicted - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

        return self

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
