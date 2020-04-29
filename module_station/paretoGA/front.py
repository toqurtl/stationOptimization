from functools import reduce
import numpy as np
from pandas import DataFrame
from pandas import ExcelWriter


# element is chromosome
class Front(list):
    def __init__(self, num_objective, rank):
        self.num_objective = num_objective
        self.rank = rank

    def chromosome_containable(self, other_chromosome):
        front_compare_list = list(map(lambda x: x == other_chromosome, self))
        return reduce(lambda equal_front_1,equal_front_2 : equal_front_1 and equal_front_2, front_compare_list)

    def _sorting_for_crowd_sorting(self):
        self.sort(key=lambda chromosome: tuple(chromosome.objectives))
        return

    def _crowd_distancing(self, objective_diff_list):
        for idx, chromosome in enumerate(self):
            # if 0 < idx < len(self)-1:
            #     crowding_distance_list = (np.array(self[idx-1].objectives) + np.array(self[idx+1].objectives))\
            #                              /np.array(objective_diff_list)
            #     chromosome.crowding_distance = crowding_distance_list.sum()
            # else:
            #     chromosome.crowding_distance = 1000
            try:
                crowding_distance_list = (np.array(self[idx - 1].objectives) + np.array(self[idx + 1].objectives)) \
                                                  / np.array(objective_diff_list)
                chromosome.crowding_distance = crowding_distance_list.sum()
            except ZeroDivisionError:
                chromosome.crowding_distance = 10000
            except IndexError:
                chromosome.crowding_distance = 10000

    def crowd_sorting(self, objective_diff_list):
        self._sorting_for_crowd_sorting()
        self._crowd_distancing(objective_diff_list)
        #descending
        self.sort(key=lambda chromosome: chromosome.crowding_distance, reverse=True)
        return

    def get_chromosome_list(self, num):
        return [chromosome for idx, chromosome in enumerate(self) if idx < num]

    def print_chromosomes(self):
        for chromosome in self:
            print(chromosome.objectives, end=',')
        print()


# element is front
class Fronts(list):
    def __init__(self, generation, num_objective):
        self.generation = generation
        self.num_objective = num_objective
        self.max_objective_list = []
        self.min_objective_list = []
        self._set_max_min_list()
        self._fronting()
        self._set_crowding_distance()
        return

    def _set_max_min_list(self):
        for idx in range(0, self.num_objective):
            chromosome_objective_list = list(map(lambda x: x.objectives[idx], self.generation))
            self.max_objective_list.append(max(chromosome_objective_list))
            self.min_objective_list.append(min(chromosome_objective_list))
        return

    def _fronting(self):
        rank = 0
        not_fronted_chromosome_list = []
        for chromosome in self.generation:
            not_fronted_chromosome_list.append(chromosome)

        infinite_check = 0
        while len(not_fronted_chromosome_list) > 0:
            infinite_check += 1
            front = Front(self.num_objective, rank)
            for chromosome_1 in not_fronted_chromosome_list:
                num_dominates = sum([1 for chromosome_2 in not_fronted_chromosome_list if chromosome_1 < chromosome_2])
                if num_dominates is 0:
                    front.append(chromosome_1)

            for chromosome in front:
                not_fronted_chromosome_list.remove(chromosome)
            rank += 1
            self.append(front)
            if infinite_check >= 1000:
                print('infinite loop in _fronting function in front.py')
                exit()

    def _set_crowding_distance(self):
        for front in self:
            objective_diff_list = np.array(self.max_objective_list)-np.array(self.min_objective_list)
            front.crowd_sorting(objective_diff_list.tolist())

    def to_pandas_dataframe(self):
        row_list = []
        for front in self:
            for chromosome in front:
                chromosome_list = []
                # chromosome_list = [front.rank] + chromosome.objectives
                chromosome_list.append(front.rank)
                for obj in chromosome.objectives:
                    if obj > 0:
                        chromosome_list.append(obj)
                    else:
                        chromosome_list.append(-1 * obj)
                row_list.append(chromosome_list)
        print_information_list=['front_id']
        for idx in range(0, self.num_objective):
            print_information_list.append('objective_'+str(idx+1))

        return DataFrame(row_list, columns=print_information_list)

    def save(self, filename):
        with ExcelWriter(filename) as writer:
            self.to_pandas_dataframe().to_excel(
                excel_writer=writer, sheet_name='front_information', header=True, index=False
            )
        return

