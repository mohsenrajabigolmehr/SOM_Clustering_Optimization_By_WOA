import numpy as np
from numpy.core.fromnumeric import shape
from scipy.spatial import distance

from sklearn.metrics import davies_bouldin_score

import Helper.ListHelper as ListHelper

class WhaleClustersOptimization():
    def __init__(self, clusters, labels, data):
        self.clusters = clusters
        self.labels = labels
        self.data = data
        self.basePoint = np.zeros(len(data[0]), dtype=int)
        
        self._nsols = 10
        self._sols = self._init_solutions() 
        self._best_solutions = []        
        self._best_solution = None
        self._b = 0.5
        self._a = 2.0
        self._a_step = 100
    
    def _init_solutions(self):
        sols = []
        size = shape(self.clusters)

        for c in range(self._nsols):
            sols.append(np.random.uniform(0, 5, size=size))
        
        return sols
        
    def get_solutions(self):
        return self._sols

    def optimize(self):
        """solutions randomly encircle, search or attack"""
        ranked_sol = self._rank_solutions()
        best_sol = ranked_sol[0]
        self._best_solution = best_sol

        # print("ranked_sol : " , shape(ranked_sol))
        # print("best_sol : " , shape(best_sol))
        #include best solution in next generation solutions
        new_sols = [best_sol]

        for s in ranked_sol[1:]:
            if np.random.uniform(0.0, 1.0) > 0.5:                                      
                A = self._compute_A()                                                     
                norm_A = np.linalg.norm(A)                                                
                if norm_A < 1.0:                                                          
                    new_s = self._encircle(s, best_sol, A)                                
                else:                                                                     
                    ###select random sol                                                  
                    random_sol = self._sols[np.random.randint(0, self._nsols - 1)]
                    new_s = self._search(s, random_sol, A)                                
            else:                                                                         
                new_s = self._attack(s, best_sol)                                         
            new_sols.append(self._constrain_solution(new_s))

        print("_sols : " , shape(self._sols))
        print("_best_solutions : " , shape(self._best_solutions))

        self._sols = np.stack(new_sols)
        self._a -= self._a_step

    

    def _constrain_solution(self, sol):
        """ensure solutions are valid wrt to constraints"""
        for item in sol:
            for x in item:
                if x < 0:
                    x = 0
                elif x > 5:
                    x = 5            
        return sol

    
    def OptimizationFunction(self, Sols):
        # print("shape Sols : ", shape(Sols))
        fitness = []
        for sol in Sols:
            # print("shape sol : ", shape(sol))
            dist = 0
            for point in sol:
                dist += distance.euclidean(self.basePoint, point)
            fitness.append(dist)
        
        return fitness
    
    def _rank_solutions(self):
        """find best solution"""
        fitness = self.OptimizationFunction(self._sols)
        sol_fitness = [(f, s) for f, s in zip(fitness, self._sols)]
   
        #best solution is at the front of the list
        ranked_sol = list(sorted(sol_fitness, key=lambda x:x[0], reverse=True))
        self._best_solutions.append(ranked_sol[0])

        return [ s[1] for s in ranked_sol] 

    def get_best_solutions(self):        
        list = sorted(self._best_solutions, key=lambda x:x[0], reverse=True)
        return list[0]

    def _compute_A(self):
        r = np.random.uniform(0.0, 1.0, size=1)
        return (2.0*np.multiply(self._a, r))-self._a

    def _compute_C(self):
        return 2.0*np.random.uniform(0.0, 1.0, size=1)
                                                                 
    def _encircle(self, sol, best_sol, A):
        D = self._encircle_D(sol, best_sol[0])
        return best_sol - np.multiply(A, D)
                                                                 
    def _encircle_D(self, sol, best_sol):
        C = self._compute_C()
        D = np.linalg.norm(np.multiply(C, best_sol)  - sol)
        return D

    def _search(self, sol, rand_sol, A):
        D = self._search_D(sol, rand_sol)
        return rand_sol - np.multiply(A, D)

    def _search_D(self, sol, rand_sol):
        C = self._compute_C()
        return np.linalg.norm(np.multiply(C, rand_sol) - sol)    

    def _attack(self, sol, best_sol):
        D = np.linalg.norm(best_sol - sol)
        L = np.random.uniform(-1.0, 1.0, size=1)
        return np.multiply(np.multiply(D,np.exp(self._b*L)), np.cos(2.0*np.pi*L))+best_sol