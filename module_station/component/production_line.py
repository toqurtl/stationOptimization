from .activity import Activity
import random
from .factory import Factory
from ..paretoGA.chromosome import get_cycle
from pandas import DataFrame
from copy import deepcopy

false_expression = ['False', 'FALSE', 'false']
print_info_list = ['act_id', 'manhour', 'min_labor', 'max_labor', 'duration']
random.seed(0)


class ProductionLine(list):
    def __init__(self, filename):
        temp_list = read_file(filename=filename)
        for temp in temp_list:
            temp_act = self.TempActivity(temp)
            self.append(Activity(temp_act=temp_act, num_labor=temp_act.min_labor))

        self.min_cycle = 32
        self.max_cycle = 255
        self.max_labor_list = self.get_max_labor_list()
        self.labor_fixed_list = self.get_labor_fixed_list()

    def get_max_labor_list(self):
        return list(map(lambda activity: activity.max_labor, self))

    def get_labor_fixed_list(self):
        return list(map(lambda activity: activity.labor_fixed, self))

    def reflect_fixed_list(self, labor_num_list):
        if len(labor_num_list) is not len(self):
            print('production_line : reflect_fixed_list')
            exit()
        else:
            for idx, activity in enumerate(self):
                if activity.labor_fixed:
                    labor_num_list[idx] = activity.num_labor
        return labor_num_list

    def random_labor_num_list(self):
        return list(map(lambda act: random.randint(act.min_labor, act.max_labor) if act.labor_fixed else act.num_labor, self))

    def set_labor_num(self, labor_num_list):
        if len(labor_num_list) is not len(self):
            print('num of labor_list is not equal to num of activity')
            return
        else:
            for act, labor_num in zip(self, labor_num_list):
                if not act.labor_fixed:
                    act.set_labor_num(labor_num)

    def create_factory(self, cycle_time, labor_num_list=None, initialize=True):
        if labor_num_list is None:
            labor_num_list = self.random_labor_num_list()
        self.set_labor_num(labor_num_list)
        factory = Factory(cycle_time=cycle_time)
        buildable = factory.build_factory(production_line=deepcopy(self), initialize=initialize)
        return buildable, factory

    def create_factory_from_chromosome(self, chromosome, initialize=True):
        cycle_time = get_cycle(chromosome)
        labor_chromosome = self.reflect_fixed_list(chromosome.labor_chromosome)
        buildable, factory = self.create_factory(
            cycle_time=cycle_time, labor_num_list=labor_chromosome, initialize=initialize)
        return buildable, factory

    def print_production_line(self):
        row_list = []
        for act in self:
            row = [act.id, act.manhour, act.min_labor, act.max_labor, act.manhour/act.min_labor]
            row_list.append(row)
        df = DataFrame(row_list, columns=print_info_list)
        print(df)
        return df

    def save_production_line(self):
        pass

    class TempActivity:
        def __init__(self, line_list):
            self.id = int(line_list[0])
            self.name = str(line_list[1])
            self.manhour = int(line_list[2])
            self.labor_type = str(line_list[3])
            if line_list[5] in false_expression:
                self.labor_fixed = False
            else:
                self.labor_fixed = bool(line_list[5])

            self.min_labor = int(line_list[4])
            self.max_labor = int(line_list[7])
            self.num_labor = int(line_list[4])
            self.location = str(line_list[6])

        def print_information(self):
            print(str(self.id), str(self.name))


def read_file(filename):
    temp_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i is not 0:
                temp_list.append(line.split(','))
    return temp_list
