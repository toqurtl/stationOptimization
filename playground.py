class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __del__(self):
        print(self.name + ' is destroyed')

    def print(self):
        print(self.name, self.age)

p1 = Person('A', 29)
p2 = Person('B', 30)
p3 = Person('C', 40)

person_list = []
person_list.append(p1)
person_list.append(p2)
person_list.append(p3)


a = person_list[2]
del a
print(a.print())