import random
import os
import logging
import datetime
import json

pathFolder = os.getcwd()
pathconfig = os.getcwd() + os.sep + "config" + os.sep
pathlogs = os.getcwd() + os.sep + "logs" + os.sep

logging.basicConfig(filename=pathlogs + '_test.log', 
        filemode='w', 
        level=logging.INFO, 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')


def readsettings(order):
    cfg = pathconfig + "settings.json"
    logging.debug('        Repertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        couleur = data[order]['couleur']
        num = data[order]['num']
        valeur = data[order]['valeur']
        
        return [couleur,num,valeur]

def loadjsonarray():
    jsonarray = []
    nbc = 33
    order = 1
    cfg = pathconfig + "settings.json"
    print("Settings conf: " + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        while order <= nbc: 
            couleur = data[str(order)]['couleur']
            num = data[str(order)]['num']
            valeur = data[str(order)]['valeur']
            jsonarray.append([order,couleur,num,valeur])
            
            if order == nbc: 
                logging.info(str(jsonarray))
                
            order += 1

        
        return jsonarray


# ===== MAIN =====
tab = loadjsonarray()
for i in tab:
    logging.info('1er niv.: ' + str(i))
    print(str(i))
    # for j in i:
    #     logging.info('2nd niv.: ' + str(j))
    #     print(str(j))

logging.info("...............> Va pour la def de sup")
# supprimer la nieme carte
n = 29 
idx = tab.pop(n -1)
logging.info('idx = tab.pop('+ str(n -1) + ') valeur de n= ' + str(n) + ' ' + str(idx))
n = 8
idx = tab.pop(n -1)
logging.info('idx = tab.pop('+ str(n -1) + ') valeur de n= ' + str(n) + ' ' + str(idx))
# tab.pop(0)
# tab.pop(20)
#tab.remove(str([33, 'Joker', '33', 'Joker']))
# tab.remove(str(10))
# tab.remove(str(20))
# tab.remove(str(30))
logging.info("...............>")
logging.info("Apres suppression d'un item: " + str(tab))

for i in tab:
    logging.info('1er niv. apres suppression: ' + str(i))
    print(str(i))  


nb=33
print(random.randint(1,nb))  
