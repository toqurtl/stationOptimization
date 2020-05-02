from .generation import Generation
from .generic import Generic
from .generic import GenericEnum
from .front import Fronts
from enum import Enum
import math
from pandas import DataFrame
from pandas import ExcelWriter
from copy import deepcopy
import pickle
from .exception import EmptyGenerationException, InfiniteLoopException


class ObjEnum(Enum):
    NUM_UNIT = 0
    NUM_LABOR = 1
    NUM_STATION = 2
    ACTIVITY_IDLE_TIME_FOR_LABOR = 3
    STATION_IDLE_TIME_FOR_LABOR = 4
    FACTORY_IDLE_TIME = 5


class OrderEnum(Enum):
    MAX = 1
    MIN = -1


class Optimizer:
    def __init__(self, production_line):
        self.generations = []
        self.objective_functions = []
        self.sorting_conditions = []
        self.production_line = production_line
        self.generic_number_dict = {}
        self.size = 100
        self.max_generation = 100
        self.generic = None
        self.initialize = True
        self.simulation_time = 1000

    def set_generic(self, generic_ratio, size=100, max_generation=100, simulation_time=10000, initialize=True, first_generation=True, generation=None):
        self.size = size
        self.max_generation = max_generation
        for generic_enum, ratio in generic_ratio.items():
            if not generic_enum == GenericEnum.GLOBAL_MUTATION:
                self.generic_number_dict[generic_enum] = math.floor(ratio * size)
        num_global_mutation = size - sum(list(self.generic_number_dict.values()))
        self.generic_number_dict[GenericEnum.GLOBAL_MUTATION] = num_global_mutation
        self.initialize = initialize
        self.generic = Generic(self.production_line)
        self.simulation_time = simulation_time
        if first_generation:
            first_generation = Generation(self.production_line, simulation_time, size, self.generic)
            first_generation.create_first_generation(self)
            first_generation.fronts = Fronts(first_generation, len(self.objective_functions))
            self.generations.append(first_generation)
        else:
            if generation == None:
                raise EmptyGenerationException
            else:
                self.generations.append(generation)
        return

    def add_objective(self, idx, order_enum):
        self.objective_functions.append((call_objective_function(idx), order_enum.value))

    def pareto_optimize(self):
        for idx in range(0, self.max_generation):
            pre_generation = self.generations[-1]

            # generate new chromosomes
            new_generation = self.get_new_generation(pre_generation)
            new_generation.aging()

            # sorting and delete chromosomes have low fitness
            self.calculate_objectives_generation(new_generation, self.simulation_time)
            new_generation.fronts = Fronts(new_generation, len(self.objective_functions))
            new_generation.sorting()

            self.generations.append(new_generation)
            best_front = new_generation.fronts[0]
            print(len(best_front))
            best_front.print_chromosomes()
            print(new_generation.num_generation, 'th generation.......')
        return

    def get_new_generation(self, pre_generation):
        new_generation = pre_generation.create_new_generation()
        for element in GenericEnum:
            generic_chromosome_list = []
            generic_function = self.generic.call_generic_function(element)
            infinite_check = 0
            while len(generic_chromosome_list) < self.generic_number_dict[element]:
                new_chromosome = generic_function(pre_generation, 1)
                new_chromosome.buildable, new_chromosome.factory = \
                    self.production_line.create_factory_from_chromosome(new_chromosome, initialize=self.initialize)
                containable = pre_generation.containable_in_generation(new_chromosome, initialize=self.initialize)
                containable_2 = True
                new_chromosome.factory.simulate(self.simulation_time)
                for generated_chromosome in generic_chromosome_list:
                    if generated_chromosome.__same__(new_chromosome):
                        containable_2 = False
                    else:
                        if generated_factory.__eq__(new_chromosome.factory):
                            print('same factory!')
                            containable_2 = False

                if new_chromosome.buildable and containable and containable_2:
                    generic_chromosome_list.append(new_chromosome)
                else:
                    del new_chromosome

                infinite_check += 1
                if infinite_check > 10000:
                    raise InfiniteLoopException
                    exit()
            for chromosome in generic_chromosome_list:
                new_generation.append(chromosome)
        return new_generation

    def calculate_objectives_chromosome(self, chromosome, simulation_time):
        if not chromosome.is_calculated:
            factory = chromosome.factory
            factory.simulate(simulation_time)
            for objective_function, extrema in self.objective_functions:
                objective_value = objective_function(factory, extrema)
                chromosome.objectives.append(objective_value)
            chromosome.is_calculated = True

    def calculate_objectives_generation(self, generation, simulation_time):
        for chromosome in generation:
            self.calculate_objectives_chromosome(chromosome, simulation_time)

    def save_generations(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self.generations, f, pickle.HIGHEST_PROTOCOL)

    def save_last_generation(self, name):
        last_generation = self.generations[-1]
        with open(name, 'wb') as f:
            pickle.dump([last_generation], f, pickle.HIGHEST_PROTOCOL)

    def save_to_excel(self, filename):
        row_list = []
        for generation in self.generations:
            for front in generation.fronts:
                for chromosome in front:
                    chro_list = deepcopy(chromosome.objectives)
                    chro_list.insert(0, generation.num_generation)
                    chro_list.insert(1, front.rank)
                    chro_list.append(chromosome.get_cycle())
                    row_list.append(chro_list)
        save_info_row = ['generation', 'front']
        for idx in range(0, len(self.objective_functions)):
            save_info_row.append('objective_'+str(idx+1))
        save_info_row.append('cycle_time')
        print(save_info_row)

        df = DataFrame(row_list, columns=save_info_row)

        with ExcelWriter(filename) as writer:
            df.to_excel(
                excel_writer=writer, sheet_name='optimize_result', header=True, index=False
            )
        return


def call_objective_function(idx):
    def get_station_idle_time_for_labor(factory, extrema):
        return factory.station_idle_time_for_labor * extrema

    def get_activity_idle_time_for_labor(factory, extrema):
        return factory.activity_idle_time_for_labor * extrema

    def get_num_station(factory, extrema):
        return factory.num_station * extrema

    def get_factory_idle_time(factory, extrema):
        return factory.factory_idle_time * extrema

    def get_num_unit(factory, extrema):
        return factory.num_unit * extrema

    def get_num_labor(factory, extrema):
        return factory.num_labor * extrema

    objective_function_list = {
        ObjEnum.NUM_UNIT: get_num_unit,
        ObjEnum.NUM_LABOR: get_num_labor,
        ObjEnum.NUM_STATION: get_num_station,
        ObjEnum.ACTIVITY_IDLE_TIME_FOR_LABOR: get_activity_idle_time_for_labor,
        ObjEnum.STATION_IDLE_TIME_FOR_LABOR: get_station_idle_time_for_labor,
        ObjEnum.FACTORY_IDLE_TIME: get_factory_idle_time
    }

    return objective_function_list.get(idx)

