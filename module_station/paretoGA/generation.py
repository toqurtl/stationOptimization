from pandas import ExcelWriter
from copy import deepcopy
from pandas import DataFrame
import numpy as np


class Generation(list):
    def __init__(self, production_line, simulation_time, num_of_chromosome, generic):
        self.num_generation = 0
        self.production_line = production_line
        self.simulation_time = simulation_time
        self.num_of_chromosome = num_of_chromosome
        self.generic = generic
        self.initialize = True
        self.fronts = None

    # if two factories from different chromosome are same, one of them can't be contained in this generation
    def containable_in_generation(self, other_chromosome, initialize=True):
        containable = True
        for chromosome in self:
            if chromosome.__same__(other_chromosome):
                containable = False
                break
        return containable

    def create_first_generation(self, optimizer):
        while len(self) < self.num_of_chromosome:
            chromosome = self.generic.get_random_chromosome()
            chromosome.buildable, chromosome.factory = \
                optimizer.production_line.create_factory_from_chromosome(chromosome, initialize=optimizer.initialize)
            self.append(chromosome)
        optimizer.calculate_objectives_generation(self, optimizer.simulation_time)
        print('first generation is generated')
        return

    def create_new_generation(self):
        new_generation = Generation(self.production_line, self.simulation_time, self.num_of_chromosome, self.generic)
        new_generation.num_generation = self.num_generation + 1
        for chromosome in self:
            new_generation.append(chromosome)
        return new_generation

    def delete_bad_chromosome(self):
        for i in range(0, self.num_of_chromosome):
            del self[len(self)-1]
        return

    def sorting(self):
        self.clear()
        for front in self.fronts:
            for chromosome in front:
                self.append(chromosome)
        self.delete_bad_chromosome()

    def to_pandas_dataframe(self):
        row_list = []
        for chromosome in (self):
            row_list.append(chromosome.get_row())
        return DataFrame(row_list)

    def print_generation(self):
        print(self.to_pandas_dataframe())

    def get_every_fronts_as_pandas(self):
        pandas_list = []
        for idx in range(0, len(self.fronts)):
            pandas_list.append(self.get_nth_front_as_pandas(idx))
        return pandas_list

    def get_best_front_as_pandas(self):
        return self.get_nth_front_as_pandas(0)

    def get_nth_front_as_pandas(self, idx):
        nth_front = self.fronts[idx]
        result_row = []
        for chromosome in nth_front:
            result_row.append(chromosome.objectives)
        result_row = np.array(result_row)
        return idx, DataFrame(data=result_row, columns=self._get_objective_columns())

    def _get_objective_columns(self):
        objectives = self[0].objectives
        columns = []
        for i in range(1,len(objectives)+1):
            columns.append('objective'+str(i))
        return columns

    def save(self, filename, num_objective_function=2):
        row_list = []
        for front in self.fronts:
            for chromosome in front:
                chromosome.front_num = front.rank

        for chromosome in self:
            chro_list = deepcopy(chromosome.objectives)
            chro_list.insert(0, self.num_generation)
            chro_list.insert(1, chromosome.front_num)
            chro_list.append(chromosome.get_cycle())
            row_list.append(chro_list)

        save_info_row = ['generation', 'front']
        for idx in range(0, num_objective_function):
            save_info_row.append('objective_' + str(idx + 1))
        save_info_row.append('cycle_time')

        df = DataFrame(row_list, columns=save_info_row)

        with ExcelWriter(filename) as writer:
            df.to_excel(
                excel_writer=writer, sheet_name='optimize_result', header=True, index=False
            )
        return

