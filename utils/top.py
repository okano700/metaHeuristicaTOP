import numpy as np

class top:
    # self.n            number of nodes
    # self.m            number of vehicles
    # self.tmax         maximum duration of each route.
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
            self.tmax = float(data[2].split(";")[1])
            self.pontos = []
            for x in data[3:]:
                if x != '':
                    self.pontos.append({'x':int(x.split(";")[0]), 'y':int(x.split(";")[1]), 'v':int(x.split(";")[2])})

            self.dist = [[0 for i in range(self.n)] for j in range(self.n)]
            self.vDist = [[0 for i in range(self.n)] for j in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    self.dist[i][j] = np.linalg.norm(np.array([self.pontos[i]['x'] - self.pontos[j]['x']])-
                                                     np.array([self.pontos[i]['y'] - self.pontos[j]['y']]))
                    self.vDist[i][j] = self.pontos[j]['v'] / (self.dist[i][j] if self.dist[i][j] != 0 else 999999)

            self.dist = np.array(self.dist)
            self.vDist = np.array(self.vDist)

if __name__ == '__main__':
    teste = top("../Data/Dang et al., (2013)/pr299_gen2_m3.txt")
    print("N")
    print(teste.n)
    print("m")
    print(teste.m)
    print("Tempo max")
    print(teste.tmax)
    print("Ponton inicial")
    print(teste.pontos[0])
    print("Matriz de adjacencia/ distancia")
    print(teste.dist)
    print("Matriz de adjacencia custo beneficio(v/distancia)")
    print(teste.vDist)
