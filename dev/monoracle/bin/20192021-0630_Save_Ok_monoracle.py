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
logging.info('________ Definition des chemins ________')
logging.info('______________ Repertoire Parent:  ' + pathFolder)
logging.info('______________ Repertoire de Config:  ' + pathconfig)
logging.info('______________ Repertoire de Logs:  ' + pathlogs)
###-----------------------------------------------------------------
###     FIN : Définition du logueur
####################################################################

def readsettings(order):
    logging.info('________ Info sur la carte ________')

    cfg = pathconfig + "settings.json"
    logging.info('______________ Repertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        couleur = data[order]['couleur']
        num = data[order]['num']
        valeur = data[order]['valeur']
        logging.info('          Read Setting Couleur: ' + couleur)
        logging.info('          Read Setting Numero: ' + num)
        logging.info('          Read Setting Valeur :' + valeur)
        return [couleur,num,valeur]

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
#       Extraire 13 cartes du paquet
#       Regarder s'il y a des As ou un Joker
#       Répéter l'opération 3x

i=1
nb = 33
final = []
while i <= 5:
        resultat = random.randint(1,nb)
        if is_exist(resultat) == True:
                resultat = random.randint(1,nb)
                i -= 1
        else:
                isas = is_as(resultat)
                #print("Is AS ou Joker: " + str(isas))
                logging.info('______Is AS ou Joker: ' + str(isas))
                if isas[2] == "As" or isas[2] == "Joker": final.append(isas[2] + " de " + isas[0])

                sav.append(resultat)
                logging.info('______Ligne ' + str(i) + ': '  + str(resultat) + ' - Le resultat est : ' + str(readsettings(str(resultat))))
                #print("Ligne " + str(i) + ": "  + str(resultat) + " - Le résultat est : " + str(readsettings(str(resultat))))
        
        i += 1

logging.info('__Num Carte: ' + str(sav))
#print(str(sav))
logging.info('__Final: ' + str(final))
print(str(final))
