import requests
from requests_ntlm import HttpNtlmAuth
import json
import os
import os.path
import logging
import zabbix_pbi
import urllib3
import datetime
import shutil
import glob

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#pathFolder = "C:\\Users\\celerierma\\OneDrive - Groupe BPCE\\00-PROJETS\\04-PBI\\RIFA\\WorkInProgress"

def get_session():
    user = 'idpbiproc'
    pwd = '!6@7Ck7!Bl7Gi7C'
    url = "http://swdcfrezd199/ReportServer"

    session = requests.Session()
    session.auth = HttpNtlmAuth(user, pwd)
    r = session.get(url)
    return [r.status_code, r.text]

#print(response.status_code)
#print("---------------")
#print(response.text)
#print(get_session[0])
#print(get_session[1])


def get_pbiversion(wsi):
    chaine1 = 'Microsoft Power BI Report Server Version '
    chaine2 = '"><title>'
    pos1 = wsi.find(chaine1) + len(chaine1)
    pos2 = wsi.find(chaine2)
    prt = wsi[pos1:pos2]
    print(prt.strip())

def createjsonfile():
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
    env = ["GGO","Dev","SWDCFRGGO874","idpbiproc","!6@7Ck7!Bl7Gi7C","15.0.1102.371"]
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
    

    file = "PBI_" + env[0] + "_" + env[2] + "_" + env[1] + ".json"
    with open(file,'w') as outfile:
        json.dump(data,outfile)

def removefiles():
    path = 'C:\\Users\\celerierma\\OneDrive - Groupe BPCE\\00-PROJETS\\04-PBI\\RIFA\\WorkInProgress\\'
    pathtemp = path + 'temp\\'
    for file in os.listdir(pathtemp):
        tmpfile = pathtemp + file
        print(tmpfile)
        os.remove(tmpfile)

def sendtorifa():
    print("")
    print("________ Send to RIFA ________")
    
    pathjson = pathFolder + '\\json\\'
    b64Val = "YWJhbHJwcm9jOnNVcFlqVDJYYVpxOEh5Qks="
    # PRD ==> 'https://operation.api.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
    # BCH ==> 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
    endpoint = 'https://operation.api.qua.intranatixis.com/referential/rifa/v1/topicSupply?topic=MDWJSN'
    
    logging.basicConfig(filename=pathFolder + '\\logs\\sendtorifa.log', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('________ Send to RIFA ________')

    for file in os.listdir(pathjson):
        jsonfile = pathjson + file
        print(jsonfile)
        with open(jsonfile) as jsonio:
            send_json = json.load(jsonio)
            postjson = requests.post(endpoint, headers=({"Authorization":"Basic %s" % b64Val}), json=send_json, verify=False).json()

def readsettings(env):
    cfg = pathFolder + "\\config\\settings.json"
    with open(cfg) as jsoncfg:
        # obtenir dictionnaire
        data = json.load(jsoncfg)
        user = data[env]['user']
        pwd = data[env]['pwd']
        env = data[env]['env']
        return [user,pwd,env]


def readenv(srv):
    cfg = pathFolder + "\\config\\settings.json"
    
    env = srv[2]

    if env == "D" or env == "B" or env == "P":
        return readsettings(env)
        
    elif env == "R" or env == "U" or env == "T":
        return readsettings("R")



def loadenv():
    cfg = os.getcwd() + os.sep + "config" + os.sep + "infra.json"
    with open(cfg) as jsoninfra:
        # obtenir dictionnaire
        data = json.load(jsoninfra)
        pathFolder = data['thepath']['dirpath']
        pathtemp = data['thepath']['temp']
        pathjson = data['thepath']['json']
        pathlogs = data['thepath']['logs']
        endpoint = data['endpoint']['bench']
        zhostgroup = [data['zhostgroup']['bench'],data['zhostgroup']['prod']]
        
        print(data)
        print(pathFolder)
        print(pathtemp)
        print(pathjson)
        print(pathlogs)
        print(endpoint)
        print(zhostgroup)

def get_datetime():
        date = datetime.datetime.now()
        date = str(date.year)+str(date.month)+str(date.day)+"-"+str(date.hour)+str(date.minute)+str(date.second) 
        return date

print(get_datetime())



#loadenv()

# print("")
# print("_____________________________________")
# print("")
# print(os.pardir)
# print(os.curdir)
# print(os.getcwd())
# print(os.getcwd())
# print(os.sep)
# print(os.getcwd() + os.sep + "config")

#strtext='<html> <head><meta charset="utf-8"><meta name="Generator" content="Microsoft Power BI Report Server Version 15.0.2.557"><title>swdcfrdy3896/ReportServer - /</title></head><body><H1>swdcfrdy3896/ReportServer - /</H1><hr><pre>    Monday, September 30, 2019 3:29 PM        &lt;dir&gt; <A HREF="?%2fReporting+ICM&amp;rs:Command=ListChildren">Reporting ICM</A>Monday, September 30, 2019 2:12 PM        &lt;dir&gt; <A HREF="?%2fSuivi+des+engagements&amp;rs:Command=ListChildren">Suivi des engagements</A></pre><hr>Microsoft Power BI Report Server Version 15.0.2.557</body></html>'
#get_pbiversion(strtext)

#createjsonfile()

#removefiles()
#sendtorifa()

#z_pbisrv = pathFolder + "\\logs\\zabbix_pbi_srv.txt"
#zabbix_pbi.get_host_list('prd-middleware_powerbi_prod,prd-middleware_powerbi_horsprod',z_pbisrv)


# def main():
#     logging.basicConfig(filename='myapp.log', level=logging.INFO)
#     logging.info('Started')
#     logging.info('Finished')

# if __name__ == '__main__':
#     main()

#print (readenv("SWDCFRPBI464"))
#print (readenv("SWUCFRPBI464"))
#print (readenv("SWBCFRPBI464"))
#print (readenv("SWPCFRPBI464"))
