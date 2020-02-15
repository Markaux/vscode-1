
# https://docs.python.org/fr/3/tutorial/classes.html

class complex:
    def __init__(self, val1, val2):
        self.v1 = val1
        self.v2 = val2
        self.v3 = val1 * val2
        self.v4 = val1 / val2

class Dog:
    tricks = []             # # mistaken use of a class variable
    kind = 'Animals'         # class variable shared by all instances
    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

    def add_trick(self, trick):
        self.tricks.append(trick)


x = complex(10, 50)
print(str(x.v1) + " x " + str(x.v2) + " = " +str(x.v3))
print(str(x.v1) + " / " + str(x.v2) + " = " +str(x.v4))

animals = ["Chien", "Chat", "serpent"]
for a in animals:
    c= Dog(a)
    print(c.kind + " : " + c.name)
    print(c.add_trick(animals))

print(c.tricks)
