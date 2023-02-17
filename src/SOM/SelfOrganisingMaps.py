from os import error
import numpy as np
import pandas as pd
from numpy.core.fromnumeric import shape
import math


class SelfOrganisingMaps:

    def __init__(self, NumberOfClusters, NetSize, Epochs=10, Alpha=0.5):

        self.Epochs = Epochs
        self.Alpha = Alpha
        self.NumberOfClusters = NumberOfClusters
        self.NetSize = NetSize
        self.Weights = np.random.uniform(low=0, high=5, size=(NumberOfClusters, NetSize))
        self.Labels = []
        print("init random weights ...", self.Weights)

    # Function here computes the winning vector
    # by Euclidean distance
    def Winner(self, DataItem):

        D0 = 0
        D1 = 0

        for i in range(len(DataItem)):

            D0 = D0 + math.pow((DataItem[i] - self.Weights[0][i]), 2)
            D1 = D1 + math.pow((DataItem[i] - self.Weights[1][i]), 2)

            if D0 > D1:
                return 0
            else:
                return 1

    # Function here updates the winning vector
    def Update(self, DataItem, J):

        for i in range(len(self.Weights)):
            self.Weights[J][i] = self.Weights[J][i] + \
                self.Alpha * (DataItem[i] - self.Weights[J][i])

    def Fit(self, Data):

        m, n = len(Data), len(Data[0])

        for i in range(self.Epochs):
            #print("epoch:", i)
            for j in range(m):

                # training sample
                DataItem = Data[j]

                # Compute winner vector
                J = self.Winner(DataItem)

                # Update winning vector
                self.Update(DataItem, J)

        self.Labels = np.zeros(m, dtype=int)

        for j in range(m):
            DataItem = Data[j]
            J = self.Winner(DataItem)
            self.Labels[j] = J
