class c_iterateur(object):
    def __init__(self, obj):
        self.obj = obj
        self.length = len(obj)
        self.count = 0

    def __iter__(self):
        return self

    def next(self):
        if self.count > self.length:
            raise StopIteration

        else:
            result = self.obj[self.count]

        self.count += 1
        return result

if __name__ == "__main__":
    chaine = [
        [
            ['hello-1.0',' My Beautifull-1.0 ','world-1.0'],
            ['hello-1.1',' My Beautifull-1.1 ','world-1.1'],
            ['hello-1.2',' My Beautifull-1.2 ','world-1.2']
        ],
        [
            ['hello-2.0',' My Beautifull-2.0 ','world-2.0'],
            ['hello-2.1',' My Beautifull-2.1 ','world-2.1'],
            ['hello-2.2',' My Beautifull-2.2 ','world-2.2']
        ],
        [
            ['hello-3.2',' My Beautifull-3.0 ','world-3.0'],
            ['hello-3.2',' My Beautifull-3.1 ','world-3.1'],
            ['hello-3.2',' My Beautifull-3.2 ','world-3.2']
        ]
    ]

    iter1 =c_iterateur(chaine).__iter__()
    try:
        for i in range(len(chaine)):
            print("Idx 1D: " + str(i) + " : " + str(iter1.next()))

            iter2 =c_iterateur(chaine[i]).__iter__()
            try:
                for j in range(len(chaine[i])):
                    print("___Idx 2D: " + str(j) + " : " + str(iter2.next()))

                    iter3 = c_iterateur(chaine[j]).__iter__()
                    try:
                        for k in range(len(chaine[j])):
                            print("______Idx 3D: " + str(k) + " : " + str(iter3.next()))
                    
                    except StopIteration:
                        print("fin d'iteration 3")
                
            except StopIteration:
                print("fin d'iteration 2")


    except StopIteration:
        print("fin d'iteration 1")

