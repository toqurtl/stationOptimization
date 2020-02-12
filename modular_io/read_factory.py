from component.activity import Activity

class temp_activity():
    def __init__(self, line_list):
        self.id = int(line_list[0])
        self.name = str(line_list[1])
        self.manhour = int(line_list[2])
        self.labor_type = str(line_list[3])
        self.labor_fixed = bool(line_list[5])
        self.min_labor = int(line_list[4])
        self.num_labor = int(line_list[4])
        self.location = str(line_list[6])
        self.max_labor = int(line_list[7])

    def print_information(self):
        print(str(self.id), str(self.name))

def read_file(filename):
    temp_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i is not 0:
                temp_list.append(line.split(','))
    activity_list = []
    for temp in temp_list:
        temp_act = temp_activity(temp)
        activity_list.append(Activity(temp_act=temp_act, num_labor=3))

    return activity_list

if __name__=='__main__':
    temp_list = read_file('../productionline.csv')
    activity_list = []
    for temp in temp_list:
        temp_act = temp_activity(temp)
        activity_list.append(Activity(temp_act=temp_act, num_labor=3))

    for act in activity_list:
        act.print_act()



