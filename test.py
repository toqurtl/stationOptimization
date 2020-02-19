import random
import time
import numpy as np
from component.activity import Activity
from component.station import Station
from component.factory import Factory
from component.production_line import ProductionLine
from enum import Enum
from paretoGA.optimizer import Optimizer
from functools import reduce
from functools import partial
from typing import List
from paretoGA.optimizer import Optimizer
from paretoGA.generic import GenericEnum
#
#
generic_ratio = {
    GenericEnum.SUPERIOR: 0.3,
    GenericEnum.SELECTION: 0.3,
    GenericEnum.CROSSOVER: 0.2,
    GenericEnum.LOCAL_MUTATION:0.1,
    GenericEnum.GLOBAL_MUTATION:0.1
}

production_line = ProductionLine('productionline.csv')
optimizer = Optimizer(production_line)
optimizer.add_objective(1, 1)
optimizer.add_objective(2, -1)
optimizer.set_generic(generic_ratio)

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


