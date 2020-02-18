import random
import time
import numpy as np
from component.activity import Activity
from component.station import Station
from component.factory import Factory
from component.production_line import ProductionLine

from paretoGA.optimizer import Optimizer
from functools import reduce
from functools import partial
from typing import List
#
#
# production_line = ProductionLine('productionline.csv')
# temp_list = production_line.random_labor_num()
# factory = Factory(cycle_time=140)
# factory.build_factory(production_line=production_line, initialize=True)
# buildable, factory = production_line.create_factory(cycle_time=47, initialize=True)

# if buildable:
#     for station in factory:
#         station.print_station()
#         station.print_labor_map()
#     factory.simulate(10000)
#     print(factory.num_station, factory.num_unit, factory.num_labor)
#     factory.save('result.xlsx')
# else:
#     print('fail to build factory, cycle time is too small')
test = [1,3,4,2,5]
test.reverse()
print(5/2)