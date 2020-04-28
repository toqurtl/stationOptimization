from component.production_line import ProductionLine
from paretoGA.optimizer import Optimizer
from paretoGA.generic import GenericEnum
from paretoGA.optimizer import ObjEnum
from paretoGA.optimizer import OrderEnum
import pickle

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
