import math
from copy import deepcopy
from component import factory


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


class Chromosome:
    def __init__(self, labor_chromosome, cycle_chromosome):
        self.labor_chromosome = deepcopy(labor_chromosome)
        self.cycle_chromosome = deepcopy(cycle_chromosome)
        self.cycle = self.get_cycle()

        self.fitness = 0
        self.cost = 0

        # for multi-objective
        self.objectives = []
        self.is_calculated = False
        self.num_dominates = 0
        self.is_front = False
        self.crowding_distance = 0

        # row data
        self.factory = None
        self.buildable = True

        #for save
        self.front_num = -1

    def __same__(self, other):
        return self.cycle_chromosome == other.cycle_chromosome and \
               self.labor_chromosome == other.labor_chromosome

    def __eq__(self, other):
        return self.objectives == other.objectives

    def __same_front__(self, other):
        return not self.__gt__(other) and not self.__lt__(other)

    def __gt__(self, other):
        check = True
        if self.objectives == other.objectives:
            check = False
        else:
            for objective_self, objective_other in zip(self.objectives, other.objectives):
                if objective_self < objective_other:
                    check = False
                    break
        return check

    def __lt__(self, other):
        check = True
        if self.objectives == other.objectives:
            check = False
        else:
            for objective_self, objective_other in zip(self.objectives, other.objectives):
                if objective_self > objective_other:
                    check = False
                    break
        return check

    def get_cycle(self):
        cycle = 0
        for i, val in enumerate(self.cycle_chromosome):
            cycle += val*math.pow(2, len(self.cycle_chromosome)-1-i)
        return cycle

    def information(self):
        print_list = self.get_row()
        print_list.append(self.get_cycle())
        return str(print_list)+str(self.objectives)

    def print_information(self):
        print(self.information())

    def get_row(self):
        return self.labor_chromosome+self.cycle_chromosome

    # def is_equaled(self, chromosome):
    #     return self.cycle_chromosome == chromosome.cycle_chromosome and \
    #            self.labor_chromosome == chromosome.labor_chromosome
    #
    # def is_ahead_of(self, other_chromosome):
    #     return self.objectives > other_chromosome.objectives



