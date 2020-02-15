

class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

# ____ MAIN ____
print("___Call class___")
rev = Reverse('spam')
print(iter(rev))
for char in rev:
    print(char)

print("___Call func___")
for char in reverse('golf'):
    print(char)

print("___Iterateur___")
chaine = [
        [
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world']
        ],
        [
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world']
        ],
        [
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world'],
            ['hello',' My Beautifull ','world']
        ]
    ]
iter1 = iter(chaine)

for i in range(len(chaine)):
    print("Idx 1D: " + str(i) + " : " + str(iter1.__next__()))
    
    iter2 = iter(chaine[i])
    for j in range(len(chaine[i])):
        print("___Idx 2D: " + str(j) + " : " + str(iter2.__next__()))

        iter3 = iter(chaine[j])
        for k in range(len(chaine[j])):
            print("______Idx 3D: " + str(k) + " : " + str(iter3.__next__()))