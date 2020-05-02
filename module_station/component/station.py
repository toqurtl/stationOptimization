from .activity import Activity
from pandas import DataFrame

separatable_time_min = 5
print_info_list = ['act_id', 'sub_id','act_duration', 'pre_act_id', 'pre_act_sub_id', 'num_labor', 'manhour', 'crashed']


class Station(list):
    def __init__(self, station_id, cycle_time):
        self.cycle_time = cycle_time
        self.station_idle_time = cycle_time
        self.id = station_id
        self.is_fulled = False
        self.last_station = False
        self.labor_map = {}
        self._activity_list = []
        self._remained_activity = []

        self.station_idle_time_for_labor = 0
        self.activity_idle_time_for_labor = 0
        self.num_labor = 0

    # build process
    def build_station(self, factory_activity_list, initialize=True):
        while not self.is_fulled:
            if len(factory_activity_list) > 0:
                self._add_activity(factory_activity_list, initialize=initialize)
            else:
                self.is_fulled = True
                self.last_station = True
        # TODO - add more station information, STIT, ATIT
        for act in self._activity_list:
            act.station_id = self.id
            act.station = self
            self.append(act)
        self.num_labor = self.num_labor_in_station()
        if self.last_station:
            self.station_idle_time = 0

        self.station_idle_time_for_labor = self._calculate_station_idle_time_for_labor()
        self.activity_idle_time_for_labor = self._calculate_activity_idle_time_for_labor()
        return

    def _calculate_station_idle_time_for_labor(self):
        return self.station_idle_time * self.num_labor

    def _calculate_activity_idle_time_for_labor(self):
        activity_idle_time_for_labor = 0
        for act in self:
            if act.pre_act is None:
                activity_idle_time_for_labor += (self.num_labor - act.num_labor) * act.duration
            else:
                pre_act = act.pre_act
                if pre_act.duration > act.duration:
                    activity_idle_time_for_labor -= act.num_labor * act.duration
                else:
                    activity_idle_time_for_labor -= pre_act.num_labor * pre_act.duration
                    activity_idle_time_for_labor += (self.num_labor - act.num_labor) * (act.duration - pre_act.duration)
        return activity_idle_time_for_labor

    def _add_activity(self, factory_activity_list, initialize=True):
        add_succeed = self._activity_addable(factory_activity_list[0], initialize=initialize)
        self.is_fulled = not add_succeed
        if add_succeed:
            del factory_activity_list[0]
            self.station_idle_time = self.cycle_time-self.calculate_duration()
            if len(self._remained_activity) > 0:
                factory_activity_list.insert(0, self._remained_activity[0])
                self._remained_activity.clear()

        return

    # build process - add activity from activity list
    def _activity_addable(self, act, initialize=True):
        add_succeed = True
        if self._containable(act):
            self._activity_list.append(act)
            self._reallocate_labor(act)
            self._handle_concurrent_activity(act, initialize=initialize)
        elif initialize and self._crashable(act):
            crashed_succeed, new_act = act.get_crashed_activity(self.station_idle_time)
            # self._activity_list.append(act.get_crashed_activity(self.station_idle_time))
            if crashed_succeed:
                self._activity_list.append(new_act)
                self._reallocate_labor(new_act)
                self._handle_concurrent_activity(new_act, initialize=initialize)
            else:
                add_succeed = False
        elif initialize and self._separatable(act):
            act_1, act_2 = self._separate_activity(act)
            self._activity_list.append(act_1)
            self._remained_activity.append(act_2)
            self._reallocate_labor(act_1)
            self._handle_concurrent_activity(act_1)
        else:
            add_succeed = False

        return add_succeed

    # add activity in build process - reallocate labor after adding activity according to station condition
    def _reallocate_labor(self, new_act):
        new_labor_type = new_act.labor_type
        new_num_labor = new_act.num_labor

        if new_labor_type not in self.labor_map.keys():
            self.labor_map[new_labor_type] = new_num_labor
        else:
            if self.labor_map[new_labor_type] < new_num_labor:
                self.labor_map[new_labor_type] = new_num_labor

        for act in self._activity_list:
            if act.labor_type == new_labor_type and not act.labor_fixed:
                act.set_labor_num(min(self.labor_map[new_labor_type], act.max_labor))

        return

    # add activity in build process - check if the activity is concurrentable with previous activity.
    # If concurrentable, reallocate labor
    def _handle_concurrent_activity(self, act, initialize=True):
        num_act = len(self._activity_list)
        labor_type = act.labor_type
        if initialize and num_act > 1:
            pre_act = self._activity_list[num_act-2]
            if act.is_concurrent_act(pre_act):
                # mark concurrent activity
                act.pre_act = pre_act
                # labor reallocation according to new situation
                if labor_type == pre_act.labor_type:
                    num_labor = act.num_labor + pre_act.num_labor
                    self.labor_map[labor_type] = num_labor
                    for temp_act in self._activity_list:
                        if act.labor_type == labor_type and not act.labor_fixed and not temp_act.is_same_activity(pre_act) and not temp_act.is_same_activity(act):
                            act.set_labor_num(min(num_labor, act.max_labor))
        return

    def _separate_activity(self, act):
        if act.duration - self.station_idle_time < separatable_time_min:
            new_manhour = act.manhour-act.required_manhour(separatable_time_min)
        else:
            new_manhour = act.required_manhour(self.station_idle_time)
        # TODO - After activity constructor is designed, change the code according to the design
        act_1 = Activity(act=act, num_labor=act.num_labor, manhour=new_manhour)
        act_2 = Activity(act=act, num_labor=act.num_labor, manhour=act.manhour-new_manhour)
        act_1.subid = act.subid
        act_2.subid = act.subid+1
        return act_1, act_2

    def _containable(self, act):
        return (self.station_idle_time >= act.duration) and (self.station_idle_time >= separatable_time_min)

    def _crashable(self, act):
        return act.crashable_in_station(self.station_idle_time) and self.station_idle_time >= separatable_time_min

    def _separatable(self, act):
        return act.duration >= 2*separatable_time_min and self.station_idle_time >= separatable_time_min

    # during/after building station, calculate settled station information
    def num_labor_in_station(self):
        num_labor = 0
        for key in self.labor_map.keys():
            num_labor += self.labor_map[key]
        return num_labor

    def calculate_STIT(self):
        num_labor = self.num_labor_in_station()
        STIT = (self.cycle_time - self.station_idle_time) * num_labor
        return STIT

    def calculate_duration(self):
        duration = 0
        idx = 0
        check = len(self._activity_list)
        while idx < check:
            act = self._activity_list[idx]
            if act.pre_act is None:
                duration += act.duration
                idx += 1
            else:
                duration -= self._activity_list[idx-1].duration
                duration += max(act.duration, act.pre_act.duration)
                idx += 1

        return duration

    def print_station(self):
        print('station id:', self.id)
        print('station_duration: ', self.calculate_duration())
        row_list = list(map(lambda act: act.get_act_row(), self))
        df = DataFrame(row_list, columns=print_info_list)
        print(df)
        return df

    def print_labor_map(self):
        df = DataFrame(list(self.labor_map.items()), columns=['labor type', 'num of labor'])
        print(df)
        return df
