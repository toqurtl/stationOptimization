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

optimizer.set_generic(generic_ratio, size=100, max_generation=50, simulation_time=10000, initialize=True)
optimizer.pareto_optimize()
optimizer.save_generations('test_evolution.ge')
generations = optimizer.generations
best_front_list = []
for i in range(0, 9):
    generation = generations[5 * i]
    empty, front = generation.get_best_front_as_pandas()
    best_front_list.append((5 * i, front))

last_generation = generations[-1]
empty, final_front = last_generation.get_best_front_as_pandas()
best_front_list.append(('final', final_front))

fig, ax = plt.subplots()
for idx, front_data in best_front_list:
    ax.scatter(
            front_data.objective1,
            -front_data.objective2,
            alpha=0.5,
            label=str(idx)+'th',
            s=10
            )
ax.legend(fontsize=8, loc='upper left')
plt.title('ScatterPlot of all chromosomes in the generation', fontsize=10)
plt.xlabel('objective1')
plt.ylabel('objective2')
plt.show()
