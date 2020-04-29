from module_station.component.production_line import ProductionLine
from module_station.paretoGA.optimizer import Optimizer
from module_station.paretoGA.generic import GenericEnum
from module_station.paretoGA.optimizer import ObjEnum
from module_station.paretoGA.optimizer import OrderEnum
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
import numpy as np

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
optimizer.add_objective(ObjEnum.FACTORY_IDLE_TIME, OrderEnum.MIN)
optimizer.set_generic(generic_ratio, size=100, max_generation=100, simulation_time=10000, initialize=True)
optimizer.pareto_optimize()
optimizer.save_generations('3dtest.ge')
generations = optimizer.generations
best_front_list = []
for i in range(0, 9):
    generation = generations[10 * i]
    empty,front = generation.get_best_front_as_pandas()
    best_front_list.append((10 * i, front))

last_generation = generations[-1]
empty, final_front = last_generation.get_best_front_as_pandas()
best_front_list.append(('final', final_front))

fig, ax = plt.subplots()
ax = fig.add_subplot(111, projection='3d')
for idx, front_data in best_front_list:
    ax.scatter(
            front_data.objective1,
            -front_data.objective2,
            -front_data.objective3,
            alpha=0.5,
            label=str(idx)+'th',
            s=10
            )
ax.legend(fontsize=8, loc='upper left')
ax.set_title('ScatterPlot of all chromosomes in the generation', fontsize=10)
ax.set_xlabel('Num_Unit')
ax.set_ylabel('Num_Labor')
ax.set_zlabel('Factory_Idle_Time')
plt.show()
