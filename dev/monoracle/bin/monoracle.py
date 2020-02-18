import random
import os
import logging
import datetime
import json

####################################################################
###     DEB : Déclaration des variables
###-----------------------------------------------------------------
# Chemin
pathFolder = os.getcwd()
pathconfig = os.getcwd() + os.sep + "config" + os.sep
pathlogs = os.getcwd() + os.sep + "logs" + os.sep

# Variables globales
sav = []
###-----------------------------------------------------------------
###     FIN : Déclaration des variables
####################################################################


####################################################################
###     DEB : Définition du logueur
###-----------------------------------------------------------------

# def get_datetime():
#         date = datetime.datetime.now()
#         date = str(date.year)+str(date.month)+str(date.day)+"-"+str(date.hour)+str(date.minute)+str(date.second) 
#         return date

# logging.basicConfig(filename=pathlogs + str(get_datetime()) + '_monoracle.log', 
#         filemode='w', 
#         level=logging.INFO, 
#         format='%(asctime)s %(message)s', 
#         datefmt='%m/%d/%Y %I:%M:%S %p')

logging.basicConfig(filename=pathlogs + '_monoracle.log', 
        filemode='w', 
        level=logging.INFO, 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info('______ Mon Oracle ________')
logging.debug('________ Definition des chemins ________')
logging.debug('______________ Repertoire Parent:  ' + pathFolder)
logging.debug('______________ Repertoire de Config:  ' + pathconfig)
logging.info('______________ Repertoire de Logs:  ' + pathlogs)
###-----------------------------------------------------------------
###     FIN : Définition du logueur
####################################################################

def readsettings(order):
    cfg = pathconfig + "settings.json"
    logging.debug('        Repertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        couleur = data[order]['couleur']
        num = data[order]['num']
        valeur = data[order]['valeur']
        logging.debug('          Read Setting Couleur: ' + couleur)
        logging.debug('          Read Setting Numero: ' + num)
        logging.debug('          Read Setting Valeur :' + valeur)
        
        logging.info('        Info sur la carte : ' + str([couleur,num,valeur]))
        return [couleur,num,valeur]

def loadjsonarray():
        jsonarray = []
        nbc = 33
        order = 1
        cfg = pathconfig + "settings.json"
        print("SETTINGS Conf: " + cfg)
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
        

def is_exist(res):
        bln = ''
        for r in sav:
                if r == res: bln =  True
                else: bln =  False
        return bln

def is_as(res):
        val = readsettings(str(res))
        carte = []
        if val[2] == "As":
                carte = val
        elif str(val[1]) == str(33):
                carte = val
        else: 
                carte.append(0)
                carte.append(0)
                carte.append(0)

        return carte


# -------- Main

# Algorythme:
#       Brasser le jeu de 32 Cartes et Mise en cache du tirage
#       La carte tirée ne peut-êytre réutiliser ==> La supprimer du cache
#       Extraire 13 cartes du paquet
#       Regarder s'il y a des As ou un Joker
#               Si oui, Supprimer la carte du paquet
#       --> Répéter l'opération 3x

logging.info('')
logging.info(' ******************************')
logging.info(' ******* Nouveau Tirage *******')
logging.info(' ******************************')

i = 1
j = 1
nb = 33
final = []
tab = []
# On fait 3 tirage
while i <= 3:
        logging.info('')
        logging.info('----------------------')
        logging.info('==> Tirage N1 : ' + str(i))

        # Charger le json dans un tableau
        tab = loadjsonarray()
        logging.info('......> Resource tab: ' + str(tab))

        # A chaque tirage, on sort du paquet 13 cartes
        while j <= 13:
                logging.info('')
                logging.info('====> Tirage N2 de N1: ' + str(i) + ' , 13 cartes aleatoire, Carte Num: ' + str(j))

                # Extraire une carte au hasard dans le range de 1 à 33
                resultat = random.randint(1,nb)
                
                # Supprimer la carte du tableau de json
                print("RESULTAT: " + str(resultat))
                idx = tab.pop(resultat -1) # Les index partent de 0
                logging.info('......> IDX: ' + str(idx))
                logging.info('......> Resource tab: ' + str(tab))
                logging.info('......> Res: ' + str(resultat))
                logging.info('......> Idx: ' + str(idx))

                # On vérifie l'existence de la carte.
                if is_exist(resultat) == True:
                        logging.info('======> La nouvelle existe deja, on recommence ...')
                        resultat = random.randint(1,nb)
                        j -= 1
                else:
                        logging.info('======> Est une nouvelle carte')
                        # On vérifie si c'est un AS ou Joker
                        isas = is_as(resultat)
                        #print("Is AS ou Joker: " + str(isas))
                        logging.info('        Est-ce un AS ou Joker  ? ' + str(isas))
                        if isas[2] == "As" or isas[2] == "Joker": 
                                logging.info("        c'est un " + str(isas[2]))
                                # Rechercher si un as ou le joker et deja sorti ?
                                #       Si oui, ne pas tenir compte de cette nouvelle carte
                                #       Si non, l'ajouter au tableau final
                                final.append(isas[2] + " de " + isas[0])


                        sav.append(resultat)
                        logging.info('        Ligne ' + str(j) + ': '  + str(resultat) + ' - Le resultat est : ' + str(readsettings(str(resultat))))
                        #print("Ligne " + str(i) + ": "  + str(resultat) + " - Le résultat est : " + str(readsettings(str(resultat))))

                j += 1
                logging.info('        Num Carte: ' + str(sav))
                #print(str(sav))
        j = 1
        i += 1

logging.info('    Final: ' + str(final))
print(str(final))
