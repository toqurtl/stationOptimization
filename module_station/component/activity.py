import math


class Activity(object):
    def __init__(self, num_labor, temp_act=None, act=None, manhour=None, crashed=False):
        self.crashed = crashed
        if act is None:
            self.id = temp_act.id
            self.subid = 0
            self.manhour = temp_act.manhour
            self.name = temp_act.name
            self.labor_fixed = temp_act.labor_fixed
            self.min_labor = temp_act.min_labor
            self.max_labor = temp_act.max_labor
            self.labor_type = temp_act.labor_type
            self.location = temp_act.location
            self.num_labor = num_labor
            self.duration = round(self.manhour * 1.0 / num_labor)
            self.pre_act = None
            self.station_id = 0
            self.station = None
        else:
            if temp_act is None:
                self.id = act.id
                self.subid = 0
                if manhour is None:
                    self.manhour = act.manhour
                else:
                    self.manhour = manhour
                self.name = act.name
                self.labor_fixed = act.labor_fixed
                self.max_labor = act.max_labor
                self.min_labor = act.min_labor
                self.labor_type = act.labor_type
                self.location = act.location
                self.num_labor = num_labor
                self.duration = round(self.manhour * 1.0 / num_labor)
                self.pre_act = None
                self.station_id = 0
                self.station = None
            else:
                print('error - activity.py - __init__')

    def __eq__(self, other):
        return self.id == other.id and self.subid == other.id and \
               self.labor_type == other.labor_type and self.num_labor == other.labor_type

    def set_labor_num(self, num_labor):
        self.num_labor = num_labor
        self.duration = round(self.manhour*1.0/num_labor)

    def required_manhour(self, required_duration):
        return math.floor(self.manhour * required_duration / self.duration)

    def crashable_in_station(self, required_duration):
        crashable = False
        if self.crashable():
            for i in range(self.num_labor+1, self.max_labor):
                check = self.manhour*1.0/i
                if check < required_duration:
                    crashable = True
                    break
        return crashable

    def get_crashed_activity(self, required_duration):
        num_labor = self.num_labor
        crashed_succeed = False
        if self.crashable_in_station(required_duration):
            for i in range(self.num_labor + 1, self.max_labor + 1):
                check = self.manhour * 1.0 / i
                if 5 < check < required_duration:
                    num_labor = i
                    crashed_succeed = True
                    break
        return crashed_succeed, Activity(act=self, num_labor=num_labor, crashed=True)

    def crashable(self):
        return self.num_labor < self.max_labor

    def is_concurrent_act(self, act):
        return (self.location is not act.location) and act.pre_act is None

    def is_same_activity(self, act):
        return act.id == self.id and act.subid == self.subid

    def get_save_act_row(self):
        if self.pre_act is None:
            row = [self.station_id, self.station.calculate_duration(), self.id, self.subid, self.duration, \
                   self.num_labor, None, None, self.labor_type, self.location]
        else:
            row = [self.station_id, self.station.calculate_duration(), self.id, self.subid, self.duration, \
                   self.num_labor, self.pre_act.id, self.pre_act.subid, self.labor_type, self.location]
        return row

    def get_act_row(self):
        if self.pre_act is None:
            row = [self.id, self.subid, self.duration, 'None', 'None', self.num_labor, self.manhour, self.crashed]
        else:
            row = [self.id, self.subid, self.duration, self.pre_act.id, self.pre_act.subid, self.num_labor, self.manhour, self.crashed]
        return row
