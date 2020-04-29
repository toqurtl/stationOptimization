import math
from .station import Station
from pandas import DataFrame
from pandas import ExcelWriter
from .exception import BuildFactoryException

buildable_threshold = 3
print_act_info_list = ['station_id', 'station_duration', 'act_id', 'act_subid', 'duration', 'num_labor',  \
                   'pre_act_id', 'pre_act_sub_id', 'labor_type', 'location']
print_factory_info_list = ['cycle_time', 'simulation_time', 'factory_idle_time', 'station_idle_time_for_labor', 'activity_idle_time_for_labor']


class Factory(list):
    def __init__(self, cycle_time):
        self.cycle_time = cycle_time
        self.simulation_time = 0

        # factory information aggregation
        self.final_activity_list = []
        self.factory_idle_time = 0
        self.station_idle_time_for_labor = 0
        self.activity_idle_time_for_labor = 0
        self.num_station = 0
        self.num_unit = 0
        self.num_labor = 0

    def __eq__(self, other):
        return self.final_activity_list == other.final_activity_list

    def build_factory(self, production_line, initialize=True):
        station_id = 0
        num_act = len(production_line)
        buildable = True
        while buildable:
            station_id += 1
            station = Station(station_id=station_id, cycle_time=self.cycle_time)
            station.build_station(factory_activity_list=production_line, initialize=initialize)
            self.append(station)
            if station.last_station:                
                self._build_aggregation()
                break
            # for debugging
            if station_id > num_act * buildable_threshold:
                raise BuildFactoryException
                buildable = False

        return buildable

    def simulate(self, simulation_time):
        self.simulation_time = simulation_time
        time = self.cycle_time*self.num_station
        self.num_unit = math.floor((self.simulation_time-time)/self.cycle_time + 1)

    def print_factory(self):
        for station in self:
            station.print_station()
        print(self.num_unit, self.num_station, self.num_station, self.cycle_time, self.factory_idle_time)
        return

    def to_pandas_dataframe(self):
        row_list = list(map(lambda act: act.get_save_act_row(), self.final_activity_list))
        return DataFrame(row_list, columns=print_act_info_list)

    def basic_info(self):
        values = [self.cycle_time, self.simulation_time, self.factory_idle_time, self.station_idle_time_for_labor, self.activity_idle_time_for_labor]
        return DataFrame([values], columns=print_factory_info_list)

    def save(self, filename):
        with ExcelWriter(filename) as writer:
            self.to_pandas_dataframe().to_excel(
                excel_writer=writer, sheet_name='activity information', header=True, index=False
            )
            self.basic_info().to_excel(
                excel_writer=writer, sheet_name='factory basic', header=True, index=False
            )
        return

    def _build_final_activity_list(self):
        for station in self:
            for act in station:
                self.final_activity_list.append(act)
        return

    def _build_aggregation(self):
        self._build_final_activity_list()
        self.num_station = len(self)
        for station in self:
            self.factory_idle_time += station.station_idle_time
            self.num_labor += station.num_labor
            self.station_idle_time_for_labor += station.station_idle_time_for_labor
            self.activity_idle_time_for_labor += station.activity_idle_time_for_labor











