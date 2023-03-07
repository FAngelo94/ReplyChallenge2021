import numpy as np
from tqdm import tqdm

class Solution:

    def __init__(self):
        self.name = ""
        self.W = 0  # width
        self.H = 0  # height

        self.N = 0  # number of buildings
        self.M = 0  # number of antennas
        self.R = 0  # reward

        self.Nx = []  # x coordinate of the building
        self.Ny = []  # y coordinate of the building
        self.Nl = []  # latency weigth of the building
        self.Nc = []  # connection weigth of the building

        self.Mr = []  # range of the antenna
        self.Mc = []  # connection of the antenna

        self.Sx = []  # x coordinate of the antenna
        self.Sy = []  # y coordinate of the antenna
        self.Sindex = []  # index of the antenna

    def print(self):
        print("W: ", self.W)
        print("H: ", self.H)
        print("N: ", self.N)
        print("M: ", self.M)
        print("R: ", self.R)
        print("Nx: ", self.Nx)
        print("Ny: ", self.Ny)
        print("Nl: ", self.Nl)
        print("Nc: ", self.Nc)
        print("Mr: ", self.Mr)
        print("Mc: ", self.Mc)
        print("Sx: ", self.Sx)
        print("Sy: ", self.Sy)

    @classmethod
    def load_problem(cls, filename):
        with open(filename, "r") as f:
            p = cls()
            p.name = filename
            p.W, p.H = [int(e) for e in f.readline().split()]
            p.N, p.M, p.R = [int(e) for e in f.readline().split()]

            p.Nx = np.zeros(p.N, dtype=np.int32)
            p.Ny = np.zeros(p.N, dtype=np.int32)
            p.Nl = np.zeros(p.N, dtype=np.int32)
            p.Nc = np.zeros(p.N, dtype=np.int32)
            for i in range(p.N):
                x, y, l, c = f.readline().split(" ")
                p.Nx[i] = x
                p.Ny[i] = y
                p.Nl[i] = l
                p.Nc[i] = c

            p.Mr = np.zeros(p.M, dtype=np.int32)
            p.Mc = np.zeros(p.M, dtype=np.int32)
            p.Sx = np.zeros(p.M, dtype=np.int32)
            p.Sy = np.zeros(p.M, dtype=np.int32)
            p.Sindex = np.zeros(p.M, dtype=np.int32)
            for j in range(p.M):
                r, c = f.readline().split(" ")
                p.Mr[j] = r
                p.Mc[j] = c
                p.Sx[j] = 0
                p.Sy[j] = 0

            return p
        
    def order_buildings(self, by='connection'):
        print('ordering buildings...')
        # orders by Nc, then by Nl
        self.Nindex = np.lexsort((self.Nc, self.Nl)) if by == 'connection' else np.lexsort((self.Nl, self.Nc))
        self.Nx = self.Nx[self.Nindex]
        self.Ny = self.Ny[self.Nindex]
        self.Nl = self.Nl[self.Nindex]
        self.Nc = self.Nc[self.Nindex]
    
    def order_antennas(self, by='connection'):
        print('ordering antennas...')
        self.Mindex = np.lexsort((self.Mc, self.Mr)) if by == 'connection' else np.lexsort((self.Mr, self.Mc))
        print('m index',self.Mindex)
        self.Mr = self.Mr[self.Mindex]
        self.Mc = self.Mc[self.Mindex]

    def dump(self, with_score=False):
        score = None
        if with_score:
            score = self.score()
        print('dumping...')
        filename = f"{self.name[:-3]}-{score}.out" if with_score else f"{self.name[:-3]}.out"
        with open(filename, "w") as f:
            f.write(f"{self.M}\n")
            for i in tqdm(range(self.M)):
                f.write(f"{self.Sindex[i]} {self.Sx[i]} {self.Sy[i]}\n")

    def score(self):
        tot_score = 0
        tot_connected = 0
        print('scoring...')
        for i in tqdm(range(self.N)):  # for each building
            best_score = 0
            connected = 0
            for j in range(self.M):  # for each antenna
                # compute manhattan distance
                dist = abs(self.Sx[j] - self.Nx[i]) + abs(self.Sy[j] - self.Ny[i])
                score = (self.Nc[i] * self.Mc[j] - self.Nl[i] * dist) if dist <= self.Mr[j] else 0
                if score > best_score:
                    best_score = score
                    connected = 1
            tot_score += best_score
            tot_connected += connected
        print(tot_score + (self.R if tot_connected == self.N else 0))
        return tot_score + (self.R if tot_connected == self.N else 0)
    
    def find_solution_antenna_in_buildings(self):
        print('finding solution...')
        for i in tqdm(range(self.M)):
            x, y = self.Nx[i], self.Ny[i]
            self.Sx[i] = x
            self.Sy[i] = y
            self.Sindex[i] = self.Mindex[i]

    def find_solution_2(self):
        '''	
        cover many cells with antennas	
        '''
        matrix = np.zeros((self.W, self.H))
        def fill_matrix(x, y, range):
            # check if x and y are in the matrix
            if(x < 0 or x >= self.W or y < 0 or y >= self.H):
                return
            if(matrix[x,y] == 0):
                matrix[x,y] = 1
                fill_matrix(x+1, y, range-1)
                fill_matrix(x-1, y, range-1)
                fill_matrix(x, y+1, range-1)
                fill_matrix(x, y-1, range-1)
        self.index = 0
        def find_antenna_position(x, y):
            # check if x and y are in the matrix
            if(x < 0 or x >= self.W or y < 0 or y >= self.H):
                return
            if self.index >= self.M:
                return
            if(matrix[x, y] == 0):
                self.Sx[self.index] = x
                self.Sy[self.index] = y
                self.Sindex[self.index] = self.Mindex[self.index]
                fill_matrix(x, y, self.Mr[self.index])
                self.index += 1
                find_antenna_position(x+self.Mr[self.index], y)
                find_antenna_position(x-self.Mr[self.index], y)
                find_antenna_position(x, y+self.Mr[self.index])
                find_antenna_position(x, y-self.Mr[self.index])
                find_antenna_position(x+self.Mr[self.index], y+self.Mr[self.index])
                find_antenna_position(x-self.Mr[self.index], y-self.Mr[self.index])
                find_antenna_position(x+self.Mr[self.index], y-self.Mr[self.index])
                find_antenna_position(x-self.Mr[self.index], y+self.Mr[self.index])
            
        print('finding solution...')
        self.order_antennas(by='range')
        startX = int(self.W / 2)
        startY = int(self.H / 2)
        find_antenna_position(startX, startY)


    def find_random_solution(self):
      solutions = []
      print('finding solution...')
      for i in tqdm(range(self.M)):
        # generate random position for each antenna but not in the same position
        x, y = np.random.randint(0, self.W), np.random.randint(0, self.H)
        while (x, y) in solutions:
            x, y = np.random.randint(0, self.W), np.random.randint(0, self.H)
        self.Sx[i] = x
        self.Sy[i] = y
        self.Sindex[i] = i
        solutions.append((x, y))