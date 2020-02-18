# -*- coding: utf-8 -*-

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

###-----------------------------------------------------------------
###     FIN : Déclaration des variables
####################################################################

####################################################################
###     DEB : Algorythme
###-----------------------------------------------------------------
# 1) Melanger
# 	1.1) Charger les cartes (settings.json) dans un tableau # jeu = [idx, N° de carte, couleur, valeur]
# 		#Attention le tableau commence à 0
# 2) Tirage (x3)
# 	2.1) Obtenir 13 cartes au hasard
# 		Tant que 1 <= 13:
# 			- Je sors un index aléatoirement. (Valeur aléatoire comprise entre 1 et 33)
# 			- L'index qui sort doit correspondre au tableau de cartes (jeu)
# 				Si l'index est présent dans le tableau, alors
# 					On extrait le champ correspondant à cette index
# 						Si cette carte est un AS ou Joker, 
# 							on la met de coté # tir = [As, couleur] ou [Joker, Joker]
# 						Sinon, on continue
				
# 				Sinon, (L'index précédemment sorti, ne doit pas ressortir /!\)
# 					L'index est déjà sorti au tour précédent.
# 					On décrémente le tour.
# 					On repasse dans la boucle (/!\ Fonction récurssive qui peut entrainer une boucle sans fin /!\)
					
# 			- On supprime la carte du jeu
# 			- On incrémente la boucle
			
# 	2.2) On répète l'opération 2 autres fois supplémentaire

# 3) On expose les cartes mises de côté
###-----------------------------------------------------------------
###     FIN : Algorythme
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

def melanger():
	logging.info('__ Melanger __')
	print("Melanger")
	jeu = []
	cfg = pathconfig + "settings.json"
	logging.debug('        Repertoire Parent:  ' + cfg)
	with open(cfg) as jsoncfg:
		# obtenir dictionnaire
		data = json.load(jsoncfg)
		#print(str(data))
		idx = 1
		while idx <= 33:
			couleur	= data[str(idx)]['couleur']
			num		= data[str(idx)]['num']
			valeur	= data[str(idx)]['valeur']
			logging.debug('          Read Setting Index: ' + str(idx))
			logging.debug('          Read Setting Couleur: ' + couleur)
			logging.debug('          Read Setting Numero: ' + num)
			logging.debug('          Read Setting Valeur :' + valeur)
			
			logging.info('        Info sur la carte : ' + str([idx,num,couleur,valeur]))
			jeu.append([idx, num, couleur, valeur])
			idx += 1

	return jeu
	
def tirage(jeu, i, j):
	res = []
	r = 1 # idx pour jeu --> Cas de la suppression
	nbc = 33 # Nb max de carte se trouvant dans le jeu. Varie en fonction du nb cartes suprimées
	i = 1 
	j = 1
	while i <= 3: # 3
		logging.info('	Tirage Num: ' + str(i))

		while j <= 13: # 13 cartes
			idx  = random.randint(1,nbc)
			for row in jeu:
				print("RRRR ==> " + str(r))
				if idx == row[0]:
					logging.info('        Index choisit : '  + str(idx))
					logging.info('        Ligne trouvée : ' + str(row))
					logging.debug('       Num Ligne trouvée : ' + str(row[1]))
					logging.info('        ------------------------------------')
					
					# SI la carte est un as ou jocker, je la garde
					if str(row[1]) == '14' or str(row[1]) == '33':
						logging.info('        Carte extraite et ajouté au tableau de sortie : ' + str(row))
						res.append(row)

					# Suppresion de la carte du jeu (Elle ne doit ressortir)
					try:
						logging.info('        Suppression de la carte extraite du tableau de jeu : ' + str(row) + " a l index: "+ str(idx - r))
						jeu.pop(idx - r)
						logging.info('        ==> Contenu du jeu apres suppression: ' + str(jeu))
						logging.info('        ____________________________________')
						r -= 1
						nbc -= 1
					except:
						logging.info('        /!\ G UNE ERREUR : ' + str(row) + " a l index: "+ str(idx - r))
							
				else:
					pass

			# Incrémente la boucle (13 cartes)		
			j += 1
		
		# Réinitialise la boucle 13 cartes
		j = 1
		# Incrément la boucle Tirage
		i += 1

	# Retourne le résultat
	return res


# ===== MAIN =====
jeu = melanger()
resultat = tirage(jeu, 1, 1) 
print(resultat)