from module_station.component.production_line import ProductionLine
from module_station.paretoGA.optimizer import Optimizer
from module_station.paretoGA.generic import GenericEnum
from module_station.paretoGA.optimizer import ObjEnum
from module_station.paretoGA.optimizer import OrderEnum
from matplotlib import pyplot as plt

generic_ratio = {
    GenericEnum.SUPERIOR: 0,
    GenericEnum.SELECTION: 0,
    GenericEnum.CROSSOVER: 0.4,
    GenericEnum.LOCAL_MUTATION: 0.4,
    GenericEnum.GLOBAL_MUTATION: 0.2
}

production_line = ProductionLine('../sample_data/productionline.csv')

optimizer = Optimizer(production_line)
optimizer.add_objective(ObjEnum.NUM_UNIT, OrderEnum.MAX)
optimizer.add_objective(ObjEnum.NUM_LABOR, OrderEnum.MIN)

optimizer.set_generic(generic_ratio, size=100, max_generation=5, simulation_time=10000, initialize=True)
optimizer.pareto_optimize()
optimizer.save_generations('test.ge')
generations = optimizer.generations
last_generation = generations[-1]
front_list = last_generation.get_every_fronts_as_pandas()
fig, ax = plt.subplots()
for idx, front_data in front_list:
    ax.scatter(
            front_data.objective1,
            -front_data.objective2,
            alpha=0.5,
            label=idx,
            s=10
            )
ax.legend(fontsize=8, loc='upper left')
plt.title('ScatterPlot of all chromosomes in the generation', fontsize=10)
plt.xlabel('objective1')
plt.ylabel('objective2')
plt.show()
