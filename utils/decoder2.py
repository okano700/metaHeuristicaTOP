from brkga_mp_ipr.types import BaseChromosome
import numpy as np
from utils import top
import time

class TOPdecoder2():

    def __init__(self, instance: top.top):
        self.instance = instance

    def decode(self, chromosome: BaseChromosome, rewrite: bool) -> float:
        tic = time.perf_counter()
        permutation = sorted((key, index) for index, key in enumerate(chromosome))

        self.instance.clear_all()

        max = [True for i in range(self.instance.m)]
        index = 1
        for i in range(self.instance.m):
            while True:
                if permutation[index][1] != 0 and permutation[index][1] != self.instance.n -1:
                    self.instance.add(permutation[index][1],i)
                    if self.instance.cost2(i) > self.instance.tmax:
                        self.instance.remove(permutation[index][1],i)
                        break
                index += 1

        return self.instance.objective_function()
