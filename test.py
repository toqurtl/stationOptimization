import random
import time
import numpy as np
from component.activity import Activity
from component.station import Station
from component.factory import Factory
from paretoGA.generic import Generic
from paretoGA.generation import Generation
from paretoGA.front import Fronts
from component.production_line import ProductionLine
from enum import Enum
from paretoGA.optimizer import Optimizer
from functools import reduce
from functools import partial
from typing import List
from paretoGA.optimizer import Optimizer
from paretoGA.generic import GenericEnum
from paretoGA.optimizer import ObjEnum
from paretoGA.optimizer import OrderEnum
import pickle
#
generic_ratio = {
    GenericEnum.SUPERIOR: 0,
    GenericEnum.SELECTION: 0,
    GenericEnum.CROSSOVER: 0.4,
    GenericEnum.LOCAL_MUTATION: 0.4,
    GenericEnum.GLOBAL_MUTATION: 0.2
}

production_line = ProductionLine('productionline.csv')

optimizer = Optimizer(production_line)
optimizer.add_objective(ObjEnum.NUM_UNIT, OrderEnum.MAX)
optimizer.add_objective(ObjEnum.NUM_LABOR, OrderEnum.MIN)
optimizer.set_generic(generic_ratio, size=100, max_generation=13, simulation_time=10000, initialize=True)
optimizer.pareto_optimize()
optimizer.save_generations('test.ge')
with open('test.ge', 'rb') as f:
    generations = pickle.load(f)
re_generation = generations[-1]
optimizer = Optimizer(production_line)
optimizer.add_objective(ObjEnum.NUM_UNIT, OrderEnum.MAX)
optimizer.add_objective(ObjEnum.NUM_LABOR, OrderEnum.MIN)
optimizer.set_generic(generic_ratio, size=100, max_generation=10, simulation_time=10000, initialize=True, first_generation=False, generation=re_generation)
optimizer.pareto_optimize()

optimizer.save('final_result_initial.xlsx')



# first_generation = Generation(production_line, 10000, 100, optimizer.generic)
# first_generation.create_first_generation(optimizer)
# first_generation.fronts = Fronts(first_generation, len(optimizer.objective_functions))
# first_generation.fronts.save('front_result.xlsx')

# factory = Factory(cycle_time=140)
# factory.build_factory(production_line=production_line, initialize=True)
# buildable, factory = production_line.create_factory(cycle_time=47, initialize=True)
#
# if buildable:
#     for station in factory:
#         station.print_station()
#         station.print_labor_map()
#     factory.simulate(10000)
#     print(factory.num_station, factory.num_unit, factory.num_labor)
#     factory.save('result.xlsx')
# else:
#     print('fail to build factory, cycle time is too small')


