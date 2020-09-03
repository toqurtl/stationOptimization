import random
import math
import time
from typing import List
from enum import Enum
from .chromosome import Chromosome


max_cycle = 255
min_cycle = 70


def cycle_to_array(cycle):
    cycle_list = []
    for i in range(0, 8):
        cycle_list.append(cycle % 2)
        cycle = cycle//2
    cycle_list.reverse()
    return cycle_list


def get_cycle(chromosome):
    cycle = 0
    for i, val in enumerate(chromosome.cycle_chromosome):
        cycle += val*math.pow(2, len(chromosome.cycle_chromosome)-1-i)
    return cycle


class GenericEnum(Enum):
    SUPERIOR = 0
    SELECTION = 1
    CROSSOVER = 2
    LOCAL_MUTATION = 3
    GLOBAL_MUTATION = 4


class Generic:
    max_labor_list: List[Chromosome]

    def __init__(self, production_line):
        self.production_line = production_line
        self.max_labor_list = production_line.get_max_labor_list()
        self.labor_fixed_list = production_line.get_labor_fixed_list()
        self.generic_function_list = {
            GenericEnum.SUPERIOR: self.superior,
            GenericEnum.SELECTION: self.selection,
            GenericEnum.CROSSOVER: self.crossover,
            GenericEnum.LOCAL_MUTATION: self.local_mutation,
            GenericEnum.GLOBAL_MUTATION: self.global_mutation,
        }

    def call_generic_function(self, generic_enum):
        return self.generic_function_list.get(generic_enum)

    def superior(self, generation, size):
        return generation[size]

    # depreciate
    def selection(self, generation, size):
        sum_of_fitness = 0
        threshold_point = 0
        selected_idx = 0
        size = len(generation)
        random.seed(0)
        for chromosome in generation:
            sum_of_fitness += chromosome.fitness

        point = random.uniform(0, 1) * sum_of_fitness

        while threshold_point < point:
            idx = random.randint(0, size-1)
            threshold_point += generation.get(idx).fitness
            selected_idx = idx
        return generation[selected_idx]

    def crossover(self, generation, size):
        num_of_chromosome = len(generation)
        chromosome_1 = generation[random.randint(0, num_of_chromosome-1)]
        chromosome_2 = generation[random.randint(0, num_of_chromosome-1)]
        random.seed(time.time())
        point_labor = random.randint(1, len(generation))
        point_cycle = random.randint(1, 6)
        new_labor_chromosome = chromosome_1.labor_chromosome[:point_labor]+chromosome_2.labor_chromosome[point_labor:]
        new_cycle_chromosome = chromosome_2.cycle_chromosome[:point_cycle]+chromosome_2.cycle_chromosome[point_cycle:]
        new_chromosome = Chromosome(new_labor_chromosome, new_cycle_chromosome)
        return new_chromosome

    def local_mutation(self, generation, size):
        num_of_chromosome = len(generation)
        range = math.floor(num_of_chromosome * 0.2)
        chromosome = generation[random.randint(0, range)]
        labor_chromosome = []
        random.seed(time.time())
        for idx, value in enumerate(self.max_labor_list):
            if bool(random.getrandbits(1)):
                d = random.choice([-1, 1])
                if 0 < value + d < self.max_labor_list[idx]:
                    changed_value = value + d
                else:
                    changed_value = value - d
                labor_chromosome.append(changed_value)
            else:
                labor_chromosome.append(value)
        cycle = get_cycle(chromosome)
        if bool(random.getrandbits(1)):
            d = random.choice([-1, 1])
            if min_cycle < cycle + d < max_cycle:
                changed_cycle = cycle + d
            else:
                changed_cycle = cycle - d
        else:
            changed_cycle = cycle

        return Chromosome(labor_chromosome, cycle_to_array(changed_cycle))

    def global_mutation(self, generation, size):
        num_activity = len(self.max_labor_list)
        labor_chromosome = []
        random.seed(time.time())
        for idx in range(0, num_activity):
            labor_chromosome.append(random.randint(1, self.max_labor_list[idx]))
        cycle_chromosome = cycle_to_array(random.randint(min_cycle, max_cycle))
        return Chromosome(labor_chromosome, cycle_chromosome)

    def get_random_chromosome(self):
        random.seed(time.time())
        num_activity = len(self.max_labor_list)
        labor_chromosome = []
        for idx in range(0, num_activity):
            labor_chromosome.append(random.randint(1, self.max_labor_list[idx]))
        cycle_chromosome = cycle_to_array(random.randint(min_cycle, max_cycle))
        return Chromosome(labor_chromosome, cycle_chromosome)




