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
optimizer.add_objective(ObjEnum.NUM_STATION, OrderEnum.MIN)
optimizer.set_generic(generic_ratio, size=100, max_generation=5, simulation_time=10000, initialize=True)
optimizer.pareto_optimize()
optimizer.save_generations('3dtest.ge')
generations = optimizer.generations
last_generation = generations[-1]
front_list = last_generation.get_every_fronts_as_pandas()

fig, ax = plt.subplots()
ax = fig.add_subplot(111, projection='3d')


for idx, front_data in front_list:
    ax.scatter(
            front_data.objective1,
            -front_data.objective2,
            -front_data.objective3,
            alpha=0.5,
            label=idx,
            s=10
            )
ax.legend(fontsize=8, loc='upper left')
ax.set_title('3d test')
ax.set_xlabel('objective_1')
ax.set_ylabel('objective_2')
ax.set_zlabel('objective_3')
plt.show()
