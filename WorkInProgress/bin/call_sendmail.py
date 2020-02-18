import class_sendmail

sm = class_sendmail

# //////////////////////////////////////////////////////////////////////////////
# Gestion du log

logfile = ['/mycloud/apps/rifa/pbi/logs/2020213-7010_get-sendtorifa_v2.log']
tabano = ''
chaine = "ANOMALIE"
for f in logfile:
        print(os.path.basename(f),)
        with open(f,"r") as fichier:
                for ligne in fichier:
                        if chaine in ligne:
                                tabano = tabano + ligne
                                print(ligne.rstrip())

# Fin de gestion du log
# //////////////////////////////////////////////////////////////////////////////

# Identification du serveur SMTP à utiliser (vous mettez le vôtre!)
# si pas d'authentification: ne pas indiquer les 2 derniers paramètres
# 25 est le port par défaut
serveur = sm.ServeurSMTP("application-qua.emea.smtp.cib.net", 25, "", "")
 
# adresse de l'expéditeur (vous!): c'est une chaine de caractères 
exped = "mbx-middleware <middleware@natixis.com>"
 
# adresse du ou des destinataire(s) direct(s): c'est une liste de chaine comportant au moins une adresse (sinon=erreur)
to = ["Marc CELERIER <marc.celerier-ext@natixis.net>"]
 
# adresse du ou des destinataire(s) en copie: c'est une liste de chaines, éventuellement vide
cc = [""]
 
# adresse du ou des destinataire(s) en copie cachée: c'est une liste de chaines, éventuellement vide
bcc = [""]
 
# sujet du mail (monolignes). Avec un encodage le permettant (ISO-8859-1, UTF-8), le sujet peut avoir des caractères accentués
sujet = "'RIFA: Anomalie.s sur serveur Power BI"
 
# corps du mail (en général multilignes). Avec un encodage le permettant (ISO-8859-1, UTF-8), le sujet peut avoir des caractères accentués
corps = tabano

# pièces jointes éventuelles (ici, [])
pjointes = logfile
 
# choix du codage: 'US-ASCII', 'ISO-8859-1', 'ISO-8859-15', 'UTF-8', None (None=application du codage par défaut)
# rappel: ISO-8859-15 permet, en plus de l'ISO-8859-1, l'utilisation du sigle de l'Euro (€)
codage = 'ISO-8859-15'
 
# type de texte: 'plain', 'html', ... Ici, c'est 'plain'
typetexte = 'plain'
 
# création du mail correctement formaté (en-tête + corps) et encodé
try:
    message = sm.MessageSMTP(exped, to, cc, bcc, sujet, corps, pjointes, codage, typetexte)
except:
    print(u"%s" % sys.exc_info()[1])
    sys.exit()
 
# envoi du mail et affichage du résultat
rep = sm.envoieSMTP(message, serveur)
print(rep)
