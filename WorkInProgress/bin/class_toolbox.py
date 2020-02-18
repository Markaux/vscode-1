
import logging
import json
import requests
import urllib3
import os
import datetime
from requests_ntlm import HttpNtlmAuth

## Suppression des warning lors de l'appel HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### Classe pour envoyer des json à RIFA
class c_sendtorifa:

    def __init__(self, dirlog):
        dt = c_date()
        logging.basicConfig(filename=dirlog + str(dt.get_datetime) + '_sendtorifa.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('________ Send to RIFA ________')    
        
    def sendtorifa(self, file):
        print("")
        print("________ Send to RIFA ________")
        
        b64Val = "YWJhbHJwcm9jOnNVcFlqVDJYYVpxOEh5Qks="
        # PRD ==> 'https://operation.api.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        # BCH ==> 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        endpoint = 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        
        with open(file) as jsonio:
            send_json = json.load(jsonio)
            postjson = requests.post(endpoint, headers=({"Authorization":"Basic %s" % b64Val}), json=send_json, verify=False).json()

        logging.info('----> Json send to Rifa: ' + file )
        return '----> Json send to Rifa: ' + file

    def sendtorifafull(self, dirpath):
        print("")
        print("________ Send to RIFA ________")
        
        pathjson = dirpath
        b64Val = "YWJhbHJwcm9jOnNVcFlqVDJYYVpxOEh5Qks="
        # PRD ==> 'https://operation.api.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        # BCH ==> 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        endpoint = 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
        
        cpt=0
        for file in os.listdir(pathjson):
            jsonfile = pathjson + file
            cpt = cpt + 1
            print(str(cpt) + ": " + jsonfile)

            with open(jsonfile) as jsonio:
                send_json = json.load(jsonio)
                postjson = requests.post(endpoint, headers=({"Authorization":"Basic %s" % b64Val}), json=send_json, verify=False).json()
            logging.info('----> ' + str(cpt) + ': Json send to Rifa: ' + file )
        
        return '----> ' + str(cpt) + ': Json send to Rifa: ' + file


class c_session:
    def __init__(self, dirlog):
        pathFolder = os.getcwd()
        pathlogs = os.getcwd() + os.sep + "logs" + os.sep
        dt = c_date()
        logging.basicConfig(filename=dirlog + str(dt.get_datetime) + '_get_session.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('________ Get Session ________')    

    def get_session(self, url, user, pwd):
        r=''
        try:
            session = requests.Session()
            session.auth = HttpNtlmAuth(user, pwd)
            r = session.get(url)
            status_code = r.status_code
            rtext = r.text
            val = "OK"
            
        except Exception as e:
            status_code = e
            rtext = "ERR"
            val = "KO"

        logging.info(str(status_code) + " : " +  url)
        logging.info(rtext)
        return [status_code,rtext, val]

class c_date:
    def __init__(self):
        self.host = "MonHostDeTest"
    
    def get_datetime(self):
        date = datetime.datetime.now()
        date = str(date.year)+str(date.month)+str(date.day)+"-"+str(date.hour)+str(date.minute)+str(date.second) 
        return date


class c_zabbix:
    pwd = 'emFiYml4'

# ##### MAIN DE TEST #####
pathFolder = os.getcwd()
pathtemp = os.getcwd() + os.sep + "temp" + os.sep
pathjson = os.getcwd() + os.sep + "json" + os.sep
pathconfig = os.getcwd() + os.sep + "config" + os.sep
pathlogs = os.getcwd() + os.sep + "logs" + os.sep

## Test envoie json à RIFA
# jsonfile = pathjson + "PBI_AJU_SWUCFRAJU149_Rec.json"
# chargement de la classe
#s = c_sendtorifa(pathlogs)
#print(s.sendtorifa(jsonfile))
#print(s.sendtorifafull(pathjson))

# ------------------------------------------
## Test GET_SESSION
#user = 'idpbiproc'
#pwd = '!6@7Ck7!Bl7Gi7C'
#url = "http://swdcfrezd199/ReportServer"
#sess = c_session(pathlogs)
#response = sess.get_session(user, pwd, url)
#print(response[0])
#print(response[1])