

class temp_activity():
    def __init__(self, line_list):
        self.id = int(line_list[0])
        self.name = str(line_list[1])
        self.manhour = int(line_list[2])
        self.labor_type = str(line_list[3])
        self.fixed = bool(line_list[5])
        if self.fixed:
            self.num_labor = int(line_list[4])
        self.location = str(line_list[6])
        self.max_labor = int(line_list[7])

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i is not 0:
                line.split(',')



if __name__=='__main__':
    read_file('../modular3.csv')
