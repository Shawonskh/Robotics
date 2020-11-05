import numpy as np


class Kalman:
    def __init__(self):
        self.z = np.zeros((2, 1))
        self.x = np.zeros((2, 1))
        self.R = np.matrix([[0.025, 0], [0, 0.025]])
        self.F = np.matrix([[1, 0], [0, 1]])
        # Try tuning this
        self.Q = np.matrix([[0.0001, 0], [0, 0.0001]])
        self.P = np.matrix([[1, 0], [0, 1]])
        self.S = np.zeros((2, 2))
        self.y = np.zeros((2, 1))
        self.K = np.zeros((2, 2))

    def getAngle(self, newAngle, newRate, dt):
        self.F[0, 1] = dt
        self.z[0, 0] = newAngle
        self.z[1, 0] = newRate

        self.P = self.F*self.P*self.F.T+self.Q
        self.x = self.F*self.x

        self.S = self.R + self.P
        self.y = self.z - self.x
        self.K = self.P*self.S.I

        self.x = self.x + self.K*self.y
        self.P = (np.identity(2)-self.K)*self.P * \
            (np.identity(2)-self.K).T + self.K*self.R*self.K.T
        return self.x[0, 0]

    def setAngle(self, newAngle):
        self.x[0, 0] = newAngle

    def setSensorNoise(self, noise, dnoise):
        self.R[0, 0] = noise
        self.R[1, 1] = dnoise

    def setProcessNoise(self, noise, dnoise):
        self.Q[0, 0] = noise
        self.Q[1, 1] = dnoise
