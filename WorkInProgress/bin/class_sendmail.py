#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3
 
import sys
import os
 
from smtplib import SMTP
 
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
 
##############################################################################
class ServeurSMTP(object):
 
    def __init__(self, adresse="", port=25, login="", mdpasse=""):
        """conserve les paramètres d'un compte mail sur un serveur SMTP"""
        self.adresse = adresse
        self.port = port
        self.login = login
        self.mdpasse = mdpasse
 
##############################################################################
class MessageSMTP(object):
 
    def __init__(self, exped="", to=(), cc=(), bcc=(), sujet="", corps="", pjointes=(), codage='UTF-8', typetexte='plain'):
        """fabrique un mail empaqueté correctement à partir des données détaillées"""
 
        #---------------------------------------------------------------------
        # correction des arguments selon leur type
 
        self.expediteur = exped
 
        if isinstance(to, str):
            to = to.split(';')
 
        if to == [] or to == ['']:
            raise ValueError("échec: pas de destinataire!")
 
        if isinstance(cc, str):
            cc = cc.split(';')
 
        if isinstance(bcc, str):
            bcc = bcc.split(';')
 
        if isinstance(pjointes, str):
            pjointes = pjointes.split(';')
 
        if codage == None or codage == "":
            codage = 'UTF-8'
 
        #---------------------------------------------------------------------
        # construction du mail à envoyer (en-tête + corps)
 
        if pjointes == []:
            # message sans pièce jointe
            msg = MIMEText(corps, typetexte, _charset=codage)
        else:
            # message "multipart" avec une ou plusieurs pièce(s) jointe(s)
            msg = MIMEMultipart('alternatives')
 
        msg['From'] = exped
        msg['To'] = ', '.join(to)
        msg['Cc'] = ', '.join(cc)
        msg['Bcc'] = ', '.join(bcc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = sujet
        msg['Charset'] = codage
        msg['Content-Type'] = 'text/' + typetexte + '; charset=' + codage
 
        if pjointes != []:
            msg.attach(MIMEText(corps, typetexte, _charset=codage))
 
            # ajout des pièces jointes
            for fichier in pjointes:
                part = MIMEBase('application', "octet-stream")
                try:
                    with open(fichier, "rb") as f:
                        part.set_payload(f.read())
                except Exception as msgerr:
                    raise ValueError ("échec à la lecture d'un fichier joint (" + msgerr + ")")
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename="%s" % (os.path.basename(fichier),))
                msg.attach(part)
 
        # compactage final du message dans les 2 cas (avec ou sans pièce(s) jointe(s))
        self.mail = msg.as_string()
 
        # construction de la liste complète de tous les destinataires (to + cc + bcc)
        self.destinataires = to
        self.destinataires.extend(cc)
        self.destinataires.extend(bcc)
 
##############################################################################
def envoieSMTP(message, serveur):
    """envoie le message correctement compacté au serveur SMTP donné"""
 
    #=========================================================================
    # connexion au serveur SMTP
    smtp = None
    try:
        smtp = SMTP(serveur.adresse, serveur.port)
    except Exception as msgerr:
        if smtp != None:
            smtp.quit()
        return "échec: serveur non reconnu: (" + str(msgerr) + ")"
 
    #=========================================================================
    # à décommenter pour avoir tous les échanges du protocole dans la console
    # smtp.set_debuglevel(1)
 
    #=========================================================================
    # ouverture de session
    if serveur.login != "":
        try:
            rep = smtp.login(serveur.login, serveur.mdpasse)
        except Exception as msgerr:
            if smtp != None:
                smtp.quit()
            return "échec: login ou mdp non reconnu (" + msgerr + ")"
 
    #=========================================================================
    # envoi du mail
    try:
        rep = smtp.sendmail(message.expediteur, message.destinataires, message.mail)
    except Exception as msgerr:
        if smtp != None:
            smtp.quit()
        return "échec à l'envoi de mail (" + msgerr + ")"
 
    #=========================================================================
    # ici, l'envoi a été réussi
    smtp.quit()
    return ""  # retourner une chaine vide est la signature d'un envoi réussi

