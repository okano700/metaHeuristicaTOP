import numpy as np
""""
Names = Antonio Augusto Rodrigues de Camargo
        Emerson Yoshiaki Okano
"""


class top:
    # self.n            number of nodes
    # self.m            number of vehicles
    # self.tmax         maximum duration of each route.
    # self.cars[i]      nodes visited by car i
    # self.pontos[i]    data of node i (x,y,v) v = value
    # self.dist[i][j]   distance from i to j
    # self.vDist[i][j]  v[j]/self.dist[i][j]



    def __init__(self, path):
        #Cria a classe Top onde o parametro passado é o caminho para o arquivo.
        #path --> string caminho do txt


        with open(path, "r") as f:
            read_data = f.read()
            data = read_data.split('\n')
            self.n = int(data[0].split(";")[1])
            self.m = int(data[1].split(";")[1])
            self.cars = [[0, self.n-1] for i in range(self.m)]
            self.tmax = float(data[2].split(";")[1])
            self.pontos = []
            self.nUsed = [int(i) for i in range(1,self.n-1)]
            for x in data[3:]:
                if x != '':
                    self.pontos.append({'x':float(x.split(";")[0]), 'y':float(x.split(";")[1]), 'v':int(x.split(";")[2])})

            self.dist = [[0 for i in range(self.n)] for j in range(self.n)]
            self.vDist = [[0 for i in range(self.n)] for j in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    self.dist[i][j] = np.linalg.norm(np.array([self.pontos[i]['x'] - self.pontos[j]['x']])-
                                                     np.array([self.pontos[i]['y'] - self.pontos[j]['y']]))
                    self.vDist[i][j] = self.pontos[j]['v'] / (self.dist[i][j] if self.dist[i][j] != 0 else 999999)

            self.dist = np.array(self.dist)
            self.vDist = np.array(self.vDist)

    def add(self, point, car):
        if car < self.m:
            if point in self.nUsed:
                self.cars[car].insert(len(self.cars[car])-1, point)
                self.nUsed.remove(point)
            else:
                print('Ponto inexistente ou ja utilizado')
        else:
            print('Carro inexistente')

    def remove(self, point, car):
        if car < self.m:
            if point in self.cars[car]:
                self.cars[car].remove(point)
                self.nUsed.append(point)
            else:
                print('Ponto nao atribuido ao carro ')
        else:
            print('Carro inexistente')

    def cost(self,car):
        cost = 0
        ant = 0
        if type(car) == int:
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
