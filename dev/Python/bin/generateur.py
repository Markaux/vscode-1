
# https://deusyss.developpez.com/tutoriels/Programmation/introduction_iterateurs_generateurs/
# https://zestedesavoir.com/tutoriels/954/notions-de-python-avancees/1-starters/2-iterables/

def mon_generateur(data):
    iterateur = iter(data)
    for idx in range(len(data)):
        yield iterateur.__next__()

if __name__ == ('__main__'):
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

    generateur1 = mon_generateur(chaine)
    #print(generateur)
    for i in generateur1:
        print("Idx 1D: " + str(i))

        generateur2 = mon_generateur(i)
        for j in generateur2:
            print("___Idx 2D: " + str(j))

        generateur3 = mon_generateur(j)
        for k in generateur3:
            print("______Idx 3D: " + str(k))