""""
Names = Antonio Augusto Rodrigues de Camargo
        Emerson Yoshiaki Okano
"""

import numpy as np
import copy
import math
import gc
import time
from tqdm import tnrange, tqdm_notebook
import tqdm


class top:
    # self.n            number of nodes
    # self.m            number of vehicles
    # self.tmax         maximum duration of each route.
    # self.cars[i]      nodes visited by car i
    # self.pontos[i]    data of node i (x,y,v) v = value
    # self.dist[i][j]   distance from i to j
    # self.vDist[i][j]  v[j]/self.dist[i][j]



    def __init__(self, path,c = ';', c2 = ';'):
        #Cria a classe Top onde o parametro passado é o caminho para o arquivo.
        #path --> string caminho do txt


        with open(path, "r") as f:
            read_data = f.read()
            data = read_data.split('\n')
            self.n = int(data[0].split(c)[1])
            self.m = int(data[1].split(c)[1])
            self.cars = [[0, self.n-1] for i in range(self.m)]
            self.tmax = float(data[2].split(c)[1])
            self.pontos = []
            self.over = [0 for i in range(self.m)]
            self.nUsed = [int(i) for i in range(1,self.n-1)]
            self.of = 0

            for x in data[3:]:
                if x != '':
                    self.pontos.append({'x':float(x.split(c2)[0]), 'y':float(x.split(c2)[1]), 'v':int(x.split(c2)[2])})

            self.dist = [[0 for i in range(self.n)] for j in range(self.n)]
            self.vDist = [[0 for i in range(self.n)] for j in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    self.dist[i][j] = np.sqrt((self.pontos[i]['x'] - self.pontos[j]['x'])**2 + (self.pontos[i]['y'] - self.pontos[j]['y'])**2)

                    #np.linalg.norm(np.array([self.pontos[i]['x'] - self.pontos[j]['x']]) - np.array([self.pontos[i]['y'] - self.pontos[j]['y']]))
                    self.vDist[i][j] = self.pontos[j]['v']**2 / (self.dist[i][j] if self.dist[i][j] != 0 else 999999)

            self.dist = np.array(self.dist)
            self.vDist = np.array(self.vDist)
            for index,dist in enumerate(self.dist[0]):
                if dist > self.tmax:
                    self.nUsed.remove(index)

    def add(self, point, car):
        if car < self.m:
            if point in self.nUsed:
                self.cars[car].insert(len(self.cars[car])-1, point)
                self.nUsed.remove(point)
            else:
                print('Ponto '+str(point)+' ja utilizado')
                print(self.cars)
                print(self.nUsed)
        else:
            print('Carro inexistente')

    def remove(self, point, car):
        if car < self.m:
            if point in self.cars[car]:
                self.cars[car].remove(point)
                self.nUsed.append(point)
            else:
                print('Ponto ',str(point),' nao atribuido ao carro ',str(car) )
        else:
            print('Carro inexistente')

    def clear_all(self):
        self.cars = [[0, self.n-1] for i in range(self.m)]
        self.over = [0 for i in range(self.m)]
        self.nUsed = [int(i) for i in range(1,self.n-1)]
        self.of = 0

    def swap(self, p1, p2, c1, c2):
        if ((c1> len(self.cars)) or (c2 > len(self.cars)) or (p1 not in self.cars[c1]) or (p2 not in self.cars[c2])):
            print('Erro de swap')
        else:
            i1 = self.cars[c1].index(p1)
            i2 = self.cars[c2].index(p2)
            self.cars[c1][i1] = p2
            self.cars[c2][i2] = p1
            #print('swap')

    def shift(self, p1,c1,c2):
        if ((c1> len(self.cars)) or (c2 > len(self.cars)) or (p1 not in self.cars[c1])):
            print('Erro de shift')
        else:
            self.remove(p1,c1)
            self.add(p1,c2)

    def cost(self,car):
        cost = 0
        ant = 0

        if (type(car) == int):
            for i in self.cars[car]:
                cost += self.dist[ant][i]
                ant = i
            cost += self.dist[i][self.n-1]
            return cost
        else:
            for i in car:
                cost += self.dist[ant][i]
                ant = i
            cost += self.dist[i][self.n-1]
            return cost
    def cost2(self,car):
        cost = 0
        ant = 0
        for i in self.cars[car]:
            cost += self.dist[ant][i]
            ant = i
        cost += self.dist[i][self.n-1]
        return cost


    def prize(self, car):
        cost = 0
        if type(car) == int:
            for i in self.cars[car]:
                cost += self.pontos[i]['v']
                #print(self.pontos[i]['v'])
            return cost
        else:
            for i in car:
                cost += self.pontos[i]['v']
            return cost


    def objective_function(self, alpha = 0.8):
        result = 0
        over = 0
        penalty = 0

        for i in self.pontos:
            penalty += i['v']
        penalty = penalty * alpha

        for i in range(self.m):
            result += self.prize(i)
            self.over[i] = 0 if (self.tmax - self.cost(i)) > 0 else abs(self.tmax - self.cost(i))
            #print(self.tmax, self.cost(i))
        #print(result, over)
        self.of = result - sum(self.over) * penalty
        return self.of


    def two_opt(self,car):
        best = self.cars[car][:]
        route = self.cars[car][:]
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route)):
                    if j - i == 1: continue  # changes nothing, skip then
                    new_route = route[:]  # Creates a copy of route
                    new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2-optSwap since j >= i we use -1
                    if self.cost(new_route) < self.cost(best):
                        best = new_route[:]
                        improved = True
                        route = best
        self.cars[car] = route
        return best

    def remove_worst(self,car, z = 'dist'):
        if len(self.cars[car]) > 2:
            if z == 'dist':
                dist = []
                #print(self.cars[car])
                for i in range(1, len(self.cars[car])-1):
                    dist.append(self.dist[self.cars[car][i-1]][self.cars[car][i]] + self.dist[self.cars[car][i]][self.cars[car][i+1]])
                    #print(i-1,i ,self.dist[self.cars[car][i-1]][self.cars[car][i]])
                    #print(i, i+1,self.dist[self.cars[car][i]][self.cars[car][i+1]])
                #print(dist)
                #print(np.argmax(dist))
                self.remove(self.cars[car][np.argmax(dist)+1], car)
            if z == 'vdist':
                dist = []
                #print(self.cars[car])
                for i in range(1, len(self.cars[car])-1):
                    dist.append(self.pontos[i]["v"]/(self.dist[self.cars[car][i-1]][self.cars[car][i]] + self.dist[self.cars[car][i]][self.cars[car][i+1]]))

                #print(dist)
                #print(np.argmax(dist))
                self.remove(self.cars[car][np.argmax(dist)+1], car)


    def check_best(self, car, z = 'dist'):
        bdist = []
        bindex = []
        if z == 'dist':
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]] - self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.cars[car] and j in self.nUsed) else np.inf for j in range(self.n)]
                bindex.append(np.argmin(dist))
                bdist.append(dist[bindex[i]])
        elif z == 'vdist':
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]]) if (j not in self.cars[car] and j in self.nUsed) else np.inf for j in range(self.n)]
                vdist = [self.pontos[j]["v"]/(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]]- self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.vDist[car] and j in self.nUsed) else 0 for j in range(self.n)]
                bindex.append(np.argmax(vdist))
                bdist.append(dist[bindex[i]])
        return bindex[np.argmin(bdist)], bdist[np.argmin(bdist)]

    def raw_best(self, car, z = 'dist'):
        bdist = []
        bindex = []
        if z == 'dist':
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]] - self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.cars[car]) else np.inf for j in range(self.n)]
                bindex.append(np.argmin(dist))
                bdist.append(dist[bindex[i]])
        elif z == 'vdist':
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]]) if (j not in self.cars[car]) else np.inf for j in range(self.n)]
                vdist = [self.pontos[j]["v"]/(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]]- self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.vDist[car]) else 0 for j in range(self.n)]
                bindex.append(np.argmax(vdist))
                bdist.append(dist[bindex[i]])
        return bindex[np.argmin(bdist)], bdist[np.argmin(bdist)]

    def RCL(self, car, alpha = 0.8, z = 'dist'):

        if z == 'dist':
            best = [self.tmax for i in range(self.n)]
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]] - self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.cars[car] and j in self.nUsed) else np.inf for j in range(self.n)]
                best = [min(b,d) for b,d in zip(best, dist)]
            treshold = best[np.argmin(best)] + alpha * (best[np.argmax(best)] - best[np.argmin(best)])
            print(treshold)
            print(best)
            vec = []
            for index, value in enumerate(best):
                if value < treshold :
                    vec.append(index)
            #return [index if value < treshold  for index, value in enumerate(best)]
            return vec
        elif z == 'vdist':
            best = [0 for i in range(self.n)]
            for i in range(len(self.cars[car])-1):
                dist = [(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]]) if (j not in self.cars[car] and j in self.nUsed) else np.inf for j in range(self.n)]
                vdist = [self.pontos[j]["v"]/(self.dist[self.cars[car][i]][j] + self.dist[j][self.cars[car][i+1]] + 1 - self.dist[self.cars[car][i]][self.cars[car][i+1]]) if (j not in self.vDist[car] and j in self.nUsed) else 0 for j in range(self.n)]
                best = [max(b,d) for b,d in zip(best, vdist)]
            treshold = best[np.argmin(best)] + alpha * (best[np.argmax(best)] - best[np.argmin(best)])
            vec = []
            for index, value in enumerate(best):
                if value > treshold :
                    vec.append(index)
            #return [index if value < treshold  for index, value in enumerate(best)]
            return vec


    def greed_start(self):

        flags = [0 for i in range(self.m)]
        while True:
            car = np.random.choice([i for i in range(self.m)])
            p, vdist = self.check_best(car,z = 'vdist')
            pd, dist = self.check_best(car,z = 'dist')
            self.add(p,car)
            self.two_opt(car)
            if (self.cost2(car)) > self.tmax:
                self.remove(p,car)
                self.two_opt(car)
                self.add(pd,car)
                self.two_opt(car)
                if self.cost2(car) > self.tmax:
                    self.remove(pd,car)
                    self.two_opt(car)
                    flags[car] = 1
            if (sum(flags) == self.m):
                self.objective_function()
                break

def semi_greed(top, alpha = 0.8, z = 'vdist', ordered = True, r = 1):
    for i in range(r):
        for car in range(len(top.cars)):
            top.add(np.random.choice(top.nUsed),car)

    if ordered:
        for i in range(len(top.cars)):
            while(top.cost(i) < top.tmax):
                top.add(np.random.choice(top.RCL(i, alpha, z)), i)
                top.two_opt(i)
            while(top.cost(i) > top.tmax):
                top.remove_worst(i,z)
                top.two_opt(i)
    else:
        flags = [0 for i in range(self.m)]
        while(True):
            car = np.random.choice([i for i in range(self.m)])
            top.add(np.random.choice(top.RCL(car, alpha, z)), car)
            top.two_opt(car)
            if self.cost2(car) > self.tmax:
                self.remove(pd,car)
                self.two_opt(car)
                flags[car] = 1
            if (sum(flags) == self.m):
                self.objective_function()
                break

def grasp_LS(top, k = 2):
    aux = copy.deepcopy(top)
    best = copy.deepcopy(aux)

    for car in range(len(top.cars)):
        for i in range(k):
            aux.remove_worst(car,z = 'vdist')
    for car in range(len(top.cars)):
        while(True):
            ponto, dist = aux.check_best(car, z = 'dist')
            if aux.cost2(car) + dist <= aux.tmax:
                aux.add(ponto,car)
                aux.two_opt(car)
            else:
                break
    if aux.objective_function()>best.objective_function():
        best = aux
    return best

def GRASP(S, tmax = 10, z = 'vdist', alpha = 0.7, k = 1, r =1):
    init = copy.deepcopy(S)
    best = copy.deepcopy(S)
    b = best.objective_function()
    start = time.perf_counter()
    log = []
    log.append(best.objective_function())
    now = time.perf_counter()
    while now < start + tmax:
        aux = copy.deepcopy(init)
        semi_greed(aux, alpha = alpha, r = r)
        aux = grasp_LS(aux, k = k)
        a = aux.objective_function()

        if a > b:
            b = a
            best = copy.deepcopy(aux)
        log.append(best.of)
        now = time.perf_counter()

    return best, log,(now - start)

def shake(S,n):
    aux = copy.deepcopy(S)
    for i in range(math.ceil(n)):
        if (aux.objective_function() < 0):
            #print(aux.over)
            for index, over in enumerate(aux.over):
                if (over > 0):
                    while(True):
                        rm = np.random.choice(aux.cars[index])
                        if (rm != 0) and (rm != (aux.n -1)):
                            aux.remove(rm,index)
                            aux.two_opt(index)
                            aux.objective_function()
                            break
        else:
            car = np.random.choice(aux.m)
            aux.add(np.random.choice(aux.nUsed), car)
            aux.two_opt(car)
            aux.objective_function()

    return aux

def local_search(S, beta = 0.3):
    aux = copy.deepcopy(S)
    n = math.ceil(beta * (sum([len(i) for i in aux.cars])))
    best = copy.deepcopy(aux)
    """
    while(any([True if len(i) == 2 else False for i in aux.cars])):
        for car, i in enumerate(aux.cars):
            if len(i) == 2:
                #print(i, car)
                aux.add(np.random.choice(aux.nUsed), car)
                aux.two_opt(car)
                aux.objective_function()
    """
    while(any([True if len(i) == 2 else False for i in aux.cars])):

        if (sum([len(j) for j in aux.cars ]) > aux.m*3):
            for car, i in enumerate(aux.cars):
                if len(i) == 2:
                    car2 = [len(j) for j in aux.cars ]
                    while(True):
                        c2 = np.argmax(car2)
                        p2 = np.random.choice(aux.cars[c2])
                        if ((p2 != 0) and (p2 != (aux.n -1))):
                            aux.shift(p2,c2,car)
                            break
        else:
            for car, i in enumerate(aux.cars):
                if len(i) == 2:
                    #print(i, car)
                    aux.add(np.random.choice(aux.nUsed), car)
                    aux.two_opt(car)
                    aux.objective_function()
                    break

    for i in range(1,n):
        car = [i for i in range(aux.m)]
        c1 = np.random.choice(car)
        car.remove(c1)
        c2 = np.random.choice(car)
        while(True):
            p1 = np.random.choice(aux.cars[c1])
            p2 = np.random.choice(aux.cars[c2])
            if ((p1 != 0) and (p2 != 0) and (p1 != (aux.n -1)) and (p2 != (aux.n -1))):
                aux.swap(p1,p2,c1,c2)
                aux.two_opt(c1)
                aux.two_opt(c2)
                if aux.objective_function() > best.of:
                    del best
                    best = copy.deepcopy(aux)
                    gc.collect()
                break
    return best

def shake2(S,n):
    aux = copy.deepcopy(S)
    for i in range(math.ceil(n)):
        options = ['add', 'remove']
        escolha = np.random.choice(options)
        if (escolha == 'add'):
            car = np.random.choice(aux.m)
            aux.add(np.random.choice(aux.nUsed), car)
            aux.two_opt(car)
            aux.objective_function()
        elif(escolha == 'remove'):
            car = np.random.choice(aux.m)
            while(True):
                if len(aux.cars[car]) == 2:
                    break
                rm = np.random.choice(aux.cars[car])
                if (rm != 0) and (rm != (aux.n -1)):
                    aux.remove(rm,car)
                    aux.two_opt(car)
                    aux.objective_function()
                    break
    return aux

def VNS(S, tmax = 10, alpha = 10, beta = 0.3):
    aux = copy.deepcopy(S)
    best = copy.deepcopy(S)
    start = time.perf_counter()
    log = []
    log.append(best.objective_function())
    now = time.perf_counter()
    while now < start + tmax:
        i = 1
        while (i < alpha):
            shakes = shake2(aux, i)
            local = local_search(shakes, beta)
            #print(local.cars)
            if local.objective_function() > aux.objective_function():
                aux = local
                if local.of > best.of:
                    best = copy.deepcopy(local)
                i = 1
                #print(i)
            else:
                i += 1
            log.append(best.of)
            #print(aux.cars)
        now = time.perf_counter()
        #print(best.of, (now - start))
    return best, log,(now - start)




def choose_neighbor(S):
    aux = copy.deepcopy(S)
    if (aux.objective_function() < 0):
        #print(aux.over)
        for index, over in enumerate(aux.over):
            if (over > 0):
                while(True):
                    rm = np.random.choice(aux.cars[index])
                    if (rm != 0) and (rm != (aux.n -1)):
                        aux.remove(rm,index)
                        aux.two_opt(index)
                        aux.objective_function()
                        break
    else:
        neighbor = np.random.choice(['add', 'remove'])
        neighbor = 'add'
        if (neighbor == 'add'):
            car = np.random.choice(aux.m)
            aux.add(np.random.choice(aux.nUsed), car)
            aux.two_opt(car)
            aux.objective_function()

        elif (neighbor == 'remove'):
            car = np.random.choice(aux.m)
            while(True):
                rm = np.random.choice(aux.cars[car])
                if (rm != 0) and (rm != (aux.n -1)):
                    aux.remove(rm,car)
                    aux.two_opt(car)
                    aux.objective_function()
                    break

    return aux

def simmulated_annealing(s0 ,T0 = 10000 ,Tf = 1 , SAmax = 1000, alpha = 0.97):

    best = s0
    s = copy.deepcopy(s0)
    T = T0
    logB = [best.of]
    log = [best.of]

    while (T > Tf):
        tic = time.perf_counter()
        print(T)
        for i in range(SAmax):
            neighbor = choose_neighbor(s)
            delta =  neighbor.objective_function() - s.objective_function()

            metropolis = math.exp(delta / T)

            if (delta > 0) or (np.random.rand() < metropolis):
                s = neighbor
                log.append(s.of)
                if (s.of > best.of):
                    best = s
                    logB.append(best.of)
            del neighbor
            gc.collect()
        toc = time.perf_counter()
        print(f"{toc - tic:0.4f} seconds")
        print("melhor", best.of)
        T = T * alpha
    return best, log, logB



if __name__ == '__main__':
    teste = top("../Data/Dang et al., (2013)/pr299_gen2_m3.txt")
    print("N")
    print(teste.n)
    print("m")
    print(teste.m)
    print("veiculos")
    print(teste.cars)
    print("Tempo max")
    print(teste.tmax)
    print("Ponton inicial")
    print(teste.pontos[0])
    print("Matriz de adjacencia/ distancia")
    print(teste.dist)
    print("Matriz de adjacencia custo beneficio(v/distancia)")
    print(teste.vDist)
