from paretoGA.generic import Generic
from paretoGA.generic import GenericEnum
from paretoGA.optimizer import Optimizer
from paretoGA.optimizer import ObjEnum
from component.production_line import ProductionLine

import numpy as np
from functools import reduce

generic_ratio = {
    GenericEnum.SUPERIOR: 0.3,
    GenericEnum.SELECTION: 0.3,
    GenericEnum.CROSSOVER: 0.2,
    GenericEnum.LOCAL_MUTATION:0.1,
    GenericEnum.GLOBAL_MUTATION:0.1
}

production_line = ProductionLine('productionline.csv')

optimizer = Optimizer(production_line)
optimizer.add_objective(ObjEnum.NUM_UNIT, 1)
optimizer.add_objective(ObjEnum.NUM_LABOR, 1)
optimizer.set_generic(generic_ratio)


chromosome_1 = optimizer.generic.get_random_chromosome()
chromosome_2 = optimizer.generic.get_random_chromosome()
# optimizer.calculate_objectives_chromosome(chromosome_1, 10000)
# optimizer.calculate_objectives_chromosome(chromosome_2, 10000)
# chromosome_1.objectives = [3,5]
# chromosome_2.objectives = [3,5]
# print(chromosome_1>chromosome_2)

a = [5,4,3]
print(a[-1])




