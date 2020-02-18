import requests
import json
import os,time,stat
import os
import csv
import shutil
import zabbix_pbi
import logging
import datetime
# Import de classe personnalisée
import class_toolbox
import class_sendmail
#___________________________________________________________________

## Initialisation de variables
csvligne = ''

## Définition des chemins
pathFolder = "/mycloud/apps/rifa/pbi" #os.getcwd()
pathtemp = pathFolder + os.sep + "temp" + os.sep
pathjson = pathFolder + os.sep + "json" + os.sep
pathconfig = pathFolder + os.sep + "config" + os.sep
pathlogs = pathFolder + os.sep + "logs" + os.sep
pbiserver = pathlogs + "infoserveurZabbix.txt"

## Host Group Zabbix
zhostgroup = 'prd-middleware_powerbi_prod,prd-middleware_powerbi_horsprod'

## Définition des variables pour envoyer un mail
to = ["Marc CELERIER <marc.celerier-ext@natixis.net>"]
cc = [""]
bcc = [""]

###-----------------------------------------------------------------
###     FIN : Définition de variables
####################################################################

####################################################################
###     DEB : Définition du logueur
###-----------------------------------------------------------------
dt = class_toolbox.c_date()
newlogfile = pathlogs + str(dt.get_datetime()) + '_get-sendtorifa_v2.log'
logging.basicConfig(filename=newlogfile, 
        filemode='w', 
        level=logging.INFO, 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p')

# logging.basicConfig(filename=pathlogs + '_get-sendtorifa_v2.log', 
#         filemode='w', 
#         level=logging.INFO, 
#         format='%(asctime)s %(message)s', 
#         datefmt='%m/%d/%Y %I:%M:%S %p')

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

# Lit les infos des servers PBI enregistre ans le json
def readpbiservers():
    logging.info('________ Parcours serverspbi.json ________')
    
    cfg = pathconfig + "serverspbi.json"
    logging.info('______________ Répertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        with open(pathlogs + 'j-pbi-servers_logs.txt', 'w') as file:
            for s in data:
                srv = data[s]['srv']
                #print(srv)
                #file.write(srv)
                file.write(srv + "\n")
        #return [srv, iua, version]

def readsettings(srv):
    logging.info('________ Parcours serverspbi.json ________')
    
    cfg = pathconfig + "serverspbi.json"
    logging.info('______________ Répertoire Parent:  ' + cfg)
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        srv = data[srv]['srv']
        iua = data[srv]['iua']
        version = data[srv]['version']
        url = data[srv]['url']
        env = data[srv]['env']
        return [iua,env,srv,url,version]

# renvoie les infos de l'environnement
def get_env(srv):
    env = srv[2]
    iua_app = srv[6:-3]

    logging.info('________ Get Env ________')
    logging.info('______________ Param 1:  ' + srv)
    logging.info('______________ Serveur:  ' + env)
    logging.info('______________ IUA APP:  ' + iua_app)

    # Retourne [iua_app,env,srv,user,pwd]
    logging.info('______________ Retour Get Env:  ' + iua_app + ' - ' + info[2] + ' - ' + srv + ' - ' + info[0] + ' - '+ info[1])

    return [iua_app,env,srv]

def compare_z_to_j():
    z = pathlogs + "infoserveurZabbix.txt"
    j = pathlogs + "j-pbi-servers_logs.txt"
    arrpbisrv = []
    with open(z) as zfile:
        for zrow in zfile.readlines():
            #print(zrow.rstrip('\n\r'))
            with open(j) as jfile:
                bln = False
                for jrow in jfile.readlines():
                    if zrow == jrow:
                        zrow = zrow.replace("\n","")
                        arrpbisrv.append([zrow])
                        # print('----------------------------')
                        # print('JSON: ' + jrow.rstrip('\n\r'))
                        # print('ZBBX: ' + zrow.rstrip('\n\r'))
                        # logging.info('COK:Z to J:JSON:' + jrow.rstrip('\n\r') + ':ZBBX:' + jrow.rstrip('\n\r'))
                        bln = True
                
                if bln == False: logging.info('ANOMALIE:Z to J:JSON:VIDE:ZBBX:' + zrow.rstrip('\n\r'))
    return arrpbisrv
                            
def compare_j_to_z():
    z = pathlogs + "infoserveurZabbix.txt"
    j = pathlogs + "j-pbi-servers_logs.txt"
    
    with open(j) as jfile:
        for jrow in jfile.readlines():
            with open(z) as zfile:
                bln = False
                for zrow in zfile.readlines():
                    if zrow == jrow: 
                        print('----------------------------')
                        print('JSON: ' + jrow.rstrip('\n\r'))
                        print('ZBBX: ' + zrow.rstrip('\n\r'))
                        logging.info('COK:J to Z:JSON:' + jrow.rstrip('\n\r') + ':' + 'ZBBX:' + zrow.rstrip('\n\r'))
                        bln = True
                
                if bln == False: logging.info('ANO:J to Z:JSON:' + jrow.rstrip('\n\r') + ':ZBBX:VIDE')


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
        "technical_version": env[4],
        "application_version": "",
        "technical_version_details": ""
    })
    logging.info(data)
    ## on peut envoyer directement le JSON sans passer par le stockage du fichier
    ##A voire ...
    file = pathjson + "PBI_" + env[0] + "_" + env[2] + "_" + env[1] + ".json"
    with open(file,'w') as outfile:
        json.dump(data,outfile)
    
    logging.info('______________ Retour json:  ' + file)
    return file

def get_info(pbisrvtab):
    logging.info('________ Get Info ________')
    
    ## On boucle sur le fichier de sortie pathFolder\logs\infoserveurZabbix.txt
    for srv in pbisrvtab:
        srv = str(srv).replace("[","")
        srv = str(srv).replace("]","")
        srv = str(srv).replace("'","")
        infoserver = readsettings(srv)
                # On crée le json
        file = createjson(infoserver)
                
        # print("===> JSON File created : " + file)
        #csvligne.writerow(["===> JSON File created : " + file])
        logging.info('===> JSON File created : " + file')

        # On envoie à RIFA le fichier json générés
        sendtorifa(file)
        logging.info('________ Sended to RIFA ________')
        print("The file: " + file + " is sended to Rifa")
        logging.info('')

# Supprime les fichiers qui n'ont pas besoin d'être historisé  
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

# Envoie les fichiers à RIFA
def sendtorifa(file):
    logging.info('________ Envoie du fichier à RIFA ' + file + ' ________')
    logging.info('______________ Appel à la classe c_sendtorifa: ')
    s = class_toolbox.c_sendtorifa(pathlogs)
    return s.sendtorifa(file)

# Supprime les fichiers de log (Rétention 7 Jours)
def removeoldlogfiles():
	heure = 60*60
	jour=24*heure
	s = 13*jour

	sup_one_week = time.time() - s
	os.chdir(pathlogs)
	for somefile in os.listdir('.'):
        	mtime=os.path.getmtime(somefile)
        	if mtime < sup_one_week:
                	os.unlink(somefile)

def sendmail(to, cc, bcc, logfile):
    # Variables pour envoie de mail
    serveur = class_sendmail.ServeurSMTP("application-qua.emea.smtp.cib.net", 25, "", "")
    exped = "mbx-middleware <middleware@natixis.com>"
    sujet = "'RIFA: Anomalie.s sur serveur Power BI"
    if logfile == '':
        pjointes = []
    else:
        pjointes = [logfile]

    codage = 'ISO-8859-15'
    typetexte = 'plain'

    # recherche des anomalies dans le fichier de log
    tabano = ''
    corps = ''
    chaine = "ANOMALIE"
    for f in pjointes:
            print(os.path.basename(f),)
            with open(f,"r") as fichier:
                    for ligne in fichier:
                            if chaine in ligne:
                                    tabano = tabano + ligne
                                    print(ligne.rstrip())

    if tabano == '':
        corps = "Pas d'anomalie"
    else:
        corps = tabano
    
    
    # création du mail correctement formaté (en-tête + corps) et encodé
    try:
        message = class_sendmail.MessageSMTP(exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte)
    except:
        print(u"%s" % sys.exc_info()[1])
        sys.exit()
    
    # envoi du mail et affichage du résultat
    rep = class_sendmail.envoieSMTP(message, serveur)
    print(rep)


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

# On lit les serveurs PBI pré-enregistrés
readpbiservers()

# On compare les infos pour n'extraire que ce qui est commun.
# Les autres sont loggués pour traitement ultérieur
pbisrvtab = compare_z_to_j()

# On collecte les infos pour créer ler json par serveur
get_info(pbisrvtab)

# Suppression des fichiers de logs > 7 jours
removeoldlogfiles()

# Envoie du mail de fin de traitement
sendmail(to, cc, bcc, newlogfile)

###-----------------------------------------------------------------
###     FIN : MAIN
####################################################################
