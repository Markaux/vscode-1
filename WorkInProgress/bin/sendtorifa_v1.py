import requests
import json
import os.path
import csv
import shutil
import zabbix_pbi
import class_toolbox
import logging
import datetime


#___________________________________________________________________

## Context root par défaut
wsi = "/ReportServer"

## Initialisation de variables
csvligne = ''

## Définition des chemins
pathFolder = os.getcwd()
pathtemp = os.getcwd() + os.sep + "temp" + os.sep
pathjson = os.getcwd() + os.sep + "json" + os.sep
pathconfig = os.getcwd() + os.sep + "config" + os.sep
pathlogs = os.getcwd() + os.sep + "logs" + os.sep
pbiserver = pathlogs + "infoserveurZabbix.txt"

## Host Group Zabbix
zhostgroup = 'prd-middleware_powerbi_prod,prd-middleware_powerbi_horsprod'

###-----------------------------------------------------------------
###     FIN : Définition de variables
####################################################################

####################################################################
###     DEB : Définition du logueur
###-----------------------------------------------------------------
dt = class_toolbox.c_date()

logging.basicConfig(filename=pathlogs + str(dt.get_datetime()) + '_filenetapi.log', 
        filemode='w', 
        level=logging.INFO, 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info('______Send To Rifa ________')
logging.info('________ Définition des chemins ________')
logging.info('______________ Répertoire Parent:  ' + pathFolder)
logging.info('______________ Répertoire Temporaire:  ' + pathtemp)
logging.info('______________ Répertoire des Json:  ' + pathjson)
logging.info('______________ Répertoire de Config:  ' + pathconfig)
logging.info('______________ Répertoire de Logs:  ' + pathlogs)
###-----------------------------------------------------------------
###     FIN : Définition du logueur
####################################################################

#___________________________________________________________________

####################################################################
###     DEB : Fonctions
###-----------------------------------------------------------------

## Récupérer la liste des serveurs se trouvant dans Zabbix ==> call zabbix_pbi.py
####   Fichier de sortie ==> pathFolder\logs\infoserveurZabbix.txt

# Lit le fichier json user/mdp/env
def readsettings(env):
    logging.info('________ Read Setting ________')
    logging.info('______________ Param 1:  ' + env)

    cfg = pathconfig + "settings.json"
    logging.info('______________ Répertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        user = data[env]['user']
        pwd = data[env]['pwd']
        env = data[env]['env']
        return [user,pwd,env]

# renvoie les infos de l'environnement
def get_env(srv):
    env = srv[2]
    iua_app = srv[6:-3]

    logging.info('________ Get Env ________')
    logging.info('______________ Param 1:  ' + srv)
    logging.info('______________ Serveur:  ' + env)
    logging.info('______________ IUA APP:  ' + iua_app)

    # Appel de la fonction readsettings(env) pour retourner les infos de connexion en fonction de l'environnement
    if env == "D" or env == "B" or env == "P":
        info = readsettings(env)
        
    elif env == "R" or env == "U" or env == "T":
        info = readsettings("R")

    # Retourne [iua_app,env,srv,user,pwd]
    logging.info('______________ Retour Get Env:  ' + iua_app + ' - ' + info[2] + ' - ' + srv + ' - ' + info[0] + ' - '+ info[1])

    return [iua_app,info[2],srv,info[0],info[1]]

def get_pbiwsi(ws, user, pwd):
    r=''
 
    logging.info('________ Get PBI WSI ________')
    logging.info('______________ Param 1:  ' + ws)
    logging.info('______________ Param 2:  ' + user)
    logging.info('______________ Param 3:  xxxxxxxx')
    
    ses = class_toolbox.c_session(pathlogs)
    return ses.get_session(ws, user, pwd)

def get_pbiversion(chaine,srv):
    logging.info('________ Get PBI Version ________')
    logging.info('______________ Param 1:  ' + chaine)
    logging.info('______________ Param 2:  ' + srv)
    #####  Le WebService retourne un html
    #####       - On extrait la version
    #####   Cas à gérer: - Quelques contexte sont différents de ReportServer
    #####                - Le serveur existe mais n'est pas configuré
    #####                - Le web service ne répond pas
    #####                - Code IUA PBI utilisé pour installer des outils tel que SSMS, VSDT, ...
    #####  Avec ces informations on construit le fichier Json
    #####       - Code IUA de la brique technique sera : PBI 
    #print(chaine)
    tmpfile = pathtemp + srv + '_wstemp.html'
    chaine1 = 'content="'
    chaine2 = 'Microsoft Power BI Report Server Version '
    chaine3 = '>'
    chaine4 = '" />'
    chaine5 = '<hr><p>HTTP Error '
    ver = ''
    
    logging.info('______________ Html temp:  ' + tmpfile)

    with open(tmpfile,'w') as file:
        file.write(chaine)
    
    with open(tmpfile,'r') as reader:
        for line in reader.readlines():
            pos1=0
            pos2=0
            ver = ""
            if line.find(chaine4) > 0:
                print("     < La ligne 1 : " + line)
                pos1 = 74 #line.find(chaine2) + len(chaine2)
                pos2 = line.find(chaine4)
                ver = line[pos1:pos2].strip()

            elif line.find(chaine1) > 0:
                print("     < La ligne 2 : " + line)
                pos1 = line.find(chaine2) + len(chaine2)
                pos2 = line.find(chaine3)
                ver = line[pos1:pos2].strip()

            if pos1 > 0:
                #print(ver)
                for c in ver:
                    if c == '"':
                        ver = ver.replace(c,'')                
                return ver
            
        # Pas de version trouvée
        logging.info('______________ Retour version:  ' + ver)
        return ver

def createjson(env):
    logging.info('________ Create Json ________')
    cpt = 0
    for p in env:
        cpt = cpt + 1
        c = str(cpt)
        if cpt != 5 :
            logging.info('______________ Param ' + c + ' : ' + p)
    # format du json: 
    # {"data": [{
    #   "application_iua":"env[0]",
    #   "environment":"env[1]",
    #   "server":"env[2]",
    #   "technical_iua":"PBI",
    #   "technical_version":"env[5]",
    #   "application_version":"",
    #   "technical_version_details":""
    # }]}
    data = {}
    data["data"] = []
    data["data"].append({
        "application_iua": env[0],
        "environment": env[1],
        "server": env[2],
        "technical_iua": "PBI",
        "technical_version": env[5],
        "application_version": "",
        "technical_version_details": ""
    })
    
    ## on peut envoyer directement le JSON sans passer par le stockage du fichier
    ##A voire ...
    file = pathjson + "PBI_" + env[0] + "_" + env[2] + "_" + env[1] + ".json"
    with open(file,'w') as outfile:
        json.dump(data,outfile)
    
    logging.info('______________ Retour json:  ' + file)
    return file

def get_info():
    logging.info('________ Get Info ________')
    
    ## On boucle sur le fichier de sortie pathFolder\logs\infoserveurZabbix.txt
    cr=''
    with open(pbiserver,"r") as f:
        with open(pathlogs + 'logs.csv', 'w', newline='') as csvfile:
            csvligne = csv.writer(csvfile, delimiter=';')
            for srv in f.readlines():
                sep = ["<-------------------------------------------------------------------------------->"]
                print(sep)
                csvligne.writerow(sep)

                ### On lit le nom serveur
                #print("<< =============== >>")
                #print(srv.strip())
                #### On extrait (Appel de fonction retournant un tableau de string [env, user, iua_app]): 
                #####       - L'environnement : 3ème lettre
                #######          - En fonction de l'environnement, on définit le user/pwd
                #####       - Le code IUA de la brique applicative 7,8,9ème lettre
                env = get_env(srv.strip())
                
                ##### Construction de l'url appelant le web service: http://<srv_name>/ReportServer
                url = "http://" + env[2] + wsi
                if env[2] == 'SWDCFRPBI511':
                    url = url + '_M62'
                elif env[2] == 'SWDCFRPBI806':
                    url = url + '_MWDEWV01'
                elif env[2] == 'SWDCFRPBI807':
                    url = url + '_BGM'
                #elif env[2] == 'SWDCFRALR101': ??????
                #    url = url + '_BGM'
                print(url)
                logging.info('______________ URL:  ' + url)

                # renvoie le webservice
                ws = get_pbiwsi(url,env[3],env[4])
                
                # Gestion du code retour si KO
                if ws[2] == "KO":
                    print("ZZZZZZZZZZZZZZZZ")
                    print("==> Check Zabbix pour : " + env[2] )
                    # Fonction retournant si c'est service ou pas (Boolean)
                    #   Call API: curl -vvv -u prd-middleware-api -k https://data.api.intranatixis.com/transaction/ision/v1/hostDetails?hostname=SWDCFRQ30166
                    #  Si c'est un Service ==> Moteur Power BI
                    #       - Installé, mais pas configuré
                    #       - Inaccessible (DMZ/FireWall)
                    #       - Service down
                    #  Si ce n'est pas un service
                    #       - C'est un serveur de developpement (SSMS, VSDT, ...) taggué sur la BT PBI
                    #           - Serveur à sortir de la BT PBI ????
                    #       - C'est un SQL Server ==> A vérifer et à transférer au DBAs
                    print("ZZZZZZZZZZZZZZZZ")


                # Code retour: 200 / 404 et 500
                cr=str(ws[0])

                # La version de PBI
                version = get_pbiversion(ws[1],env[2])
               
                # On ajoute la version à la liste env
                env.append(version)
                
                # -- Log pour debug
                logdebug = url + " - " + cr + " - " + env[0] + " - " + env[1] + " - " + env[2]  + " - " + env[3] + " / xxxxxxxx - " + env[5]
                print(logdebug)
                logging.info('______________ Log pour debug:  ' + logdebug)
                cpt=0
                ver = [cr, url,version]
                csvligne.writerow(ver)
                csvligne.writerow(env)
                for l in ver:
                    cpt = cpt + 1
                    c = str(cpt)
                    if cpt != 8 :
                        logging.info('______________ Log pour debug Ver List ' + c +' : ' + l)
                    else:
                        logging.info('______________ Log pour debug Ver List ' + c +' : xxxxxxxx')

                for l in env:
                    cpt = cpt + 1
                    c = str(cpt)
                    if cpt != 8 :
                        logging.info('______________ Log pour debug Env List ' + c +' : ' + l)
                    else:
                        logging.info('______________ Log pour debug Env List ' + c +' : xxxxxxxx')
                
                # On crée le json
                file = createjson(env)
                
                print("===> JSON File created : " + file)
                csvligne.writerow(["===> JSON File created : " + file])

                ## On envoie à RIFA le fichier json générés
                sendtorifa(file)
                csvligne.writerow(["________ Send to RIFA ________"])
                print("")
                csvligne.writerow([''])

def removefiles():
    logging.info('________ Suppression des fichiers précédemment utilisés ________')    
    for file in os.listdir(pathtemp):
        filet=pathtemp + file
        os.remove(filet)
        logging.info('______________ Répertoire temporaire:  ' + filet)
    for file in os.listdir(pathjson):
        filej=pathjson + file
        os.remove(filej)
        logging.info('______________ Répertoire Json:  ' + filej)
    
def sendtorifa(file):
    logging.info('________ Envoie du fichier à RIFA ________')
    logging.info('______________ Appel à la classe c_sendtorifa: ')
    s = class_toolbox.c_sendtorifa(pathlogs)
    return s.sendtorifa(file)

###-----------------------------------------------------------------
###     FIN : Fonctions
####################################################################

#___________________________________________________________________

####################################################################
###     DEB : MAIN
###-----------------------------------------------------------------

# Ré-initialisation des répertoires temporaires ./temp et ./json
removefiles()

# Load pbi server from Zabxix
z_pbisrv = pbiserver
zabbix_pbi.get_host_list(zhostgroup,z_pbisrv)

# On collecte les infos pour créer ler json par serveur
get_info()

###-----------------------------------------------------------------
###     FIN : MAIN
####################################################################
