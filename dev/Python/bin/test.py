

def boucle():
    i=0
    nb = 13
    while i <= nb:
        if i == 2:
            print("Deux")
        elif i == 7:
            print("Sept")
        elif i == 11:
            print("Onze")
        else:
            print(i)
        i += 1

def compare_ztoj():
    print("")

def compare_jtoz():
    print("")

def compare(arr1, arr2):
    arr3 = []
    for i in arr1:
        for j in arr2:
            if i == j:arr3.append(j)

    return arr3

# ====== Main
tab1 = [1, 2, 3, 5]
tab2 = [2, 4, 5, 10]
tab3 = []
tab3 = compare(tab1, tab2)
print(str(tab3))
print(str(tab3))
