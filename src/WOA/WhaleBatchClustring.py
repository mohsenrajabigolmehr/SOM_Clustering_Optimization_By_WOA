import re
import sys
import numpy as np
import random as random
from numpy.core.fromnumeric import partition, shape
from scipy.spatial import distance


from sklearn.utils.validation import check_X_y


class WhaleBatchClustring():

    def __init__(self, NumberOfAgents, NumberOfClusters, BatchSize):
        self.NumberOfClusters = NumberOfClusters
        self.BatchSize = BatchSize

        self.cluster_centers_ = []
        self.Labels = []

        self.a = 0
        self.A = 0
        self.C = 0
        self.I = 0
        self.p = 0

        self.b = 2.0

        self.MaxIteration = 100

        self.AgentsIsInit = False
        self.NumberOfAgents = NumberOfAgents
        self.Solutions = []
        self.SolutionsFitness = []
        self.BestSolution = 0
        self.BestSolutionIndex = 0

    def PartialFit(self, matrix):
        self.InitAgents(matrix)

        self.Labels = np.zeros((self.NumberOfAgents, len(matrix)), dtype=int)
        distances = np.zeros((1, len(matrix)), dtype=int)

        for i in range(self.MaxIteration):
            for a in range(self.NumberOfAgents):
                index = 0
                for item in matrix:
                    min_distance = sys.maxsize
                    best_cluster = 0
                    for c in range(self.NumberOfClusters):
                        solution = self.Solutions[a]
                        distance = self.CalculateEuclideanDistance(
                            item, solution[c])
                        if(distance <= min_distance):
                            min_distance = distance
                            best_cluster = c

                    self.SolutionsFitness[a] += min_distance
                    # Assign item to closest cluster
                    self.Labels[a][index] = best_cluster

                    index += 1
                    # Calculate Fitness
                    self.CalculateFitness()

            # X Is Best Search Agent
            # print(self.BestSolution)

            self.a = i

            for a in range(self.NumberOfAgents):

                self.Compute_A()
                self.Compute_C()
                self.Compute_p()

                # print(self.p)


                if(self.p < 0.5):
                    if(abs(self.A) < 1):
                        self.UpdateSearchAgent_Encircle(self.Solutions, self.BestSolution, self.A)
                    elif(abs(self.A) >= 1):
                        rand_sol = random.choice(self.Solutions)
                        self.UpdateSearchAgent_Search(self.Solutions, rand_sol, self.A)
                elif(self.p >= 0.5):
                    self.UpdateSearchAgent_Attack(self.Solutions, self.BestSolution)
                # print(i)

        return self

    def InitAgents(self, matrix):        
        if(self.AgentsIsInit == False):
            print("InitAgents")
            self.Solutions = []
            self.SolutionsFitness = []
            for a in range(self.NumberOfAgents):
                solution = np.zeros(
                    (self.NumberOfClusters, len(matrix[0])), dtype=int)
                for c in range(self.NumberOfClusters):
                    solution[c] = random.choice(matrix)
                self.Solutions.append(solution)
                self.SolutionsFitness.append(0)
            self.AgentsIsInit = True

    def CalculateEuclideanDistance(self, a, b):
        dist = distance.euclidean(a, b)
        return dist

    def CalculateFitness(self):
        # Fitness is All distances for all points of it owns cluster
        fitness = sys.maxsize
        for a in range(self.NumberOfAgents):
            if(self.SolutionsFitness[a] <= fitness):
                fitness = self.SolutionsFitness[a]
                self.BestSolution = self.Solutions[a]
                self.BestSolutionIndex = a
        return fitness

    def Compute_A(self):
        r = np.random.uniform(0.0, 1.0, size=1)
        self.A = (2.0 * np.multiply(self.a, r)) - self.a
        return self.A 

    def Compute_C(self):
        self.C = 2.0 * np.random.uniform(0.0, 1.0, size=1)
        return self.C

    def Compute_p(self):
        self.p = np.random.uniform(0.0, 1.0, size=1)
        return self.p

    def UpdateSearchAgent_Encircle(self, sol, best_sol, A):
        D = self.UpdateSearchAgent_Encircle_D(sol, best_sol)
        return best_sol - np.multiply(A, D)

    def UpdateSearchAgent_Encircle_D(self, sol, best_sol):
        C = self.Compute_C()
        D = np.linalg.norm(np.multiply(C, best_sol) - sol)
        return D

    def UpdateSearchAgent_Search(self, sol, rand_sol, A):
        D = self.UpdateSearchAgent_Search_D(sol, rand_sol)
        return rand_sol - np.multiply(A, D)

    def UpdateSearchAgent_Search_D(self, sol, rand_sol):
        C = self.Compute_C()
        return np.linalg.norm(np.multiply(C, rand_sol) - sol)

    def UpdateSearchAgent_Attack(self, sol, best_sol):
        D = np.linalg.norm(best_sol - sol)
        L = np.random.uniform(-1.0, 1.0, size=1)
        return np.multiply(np.multiply(D, np.exp(self.b*L)), np.cos(2.0*np.pi*L))+best_sol
