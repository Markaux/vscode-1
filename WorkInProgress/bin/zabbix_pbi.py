import logging
import re
import requests
import json
import os


class ZabbixService:
    
    def __init__(self):
        pathFolder = os.getcwd()
        pathlogs = os.getcwd() + os.sep + "logs" + os.sep
        logging.basicConfig(filename=pathlogs +  'get_zabbix_sevice.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('________ Get Zabbix Service ________')

        self.host = "https://zabbix.intranatixis.com/api_jsonrpc.php"
        self.user = "prd-middleware-api"

        logging.info(self.host)
        logging.info(self.user)

        password = 'zabbix' # CFN='emFiYml4' ?????

        auth_payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": password
            },
            "id": 0,
            "auth": None
        }
        auth_payload_json = json.dumps(auth_payload)

        headers = {"Content-Type": "application/json-rpc"}
        r = requests.post(self.host, data=auth_payload_json, headers=headers, verify=False)

        self.token = r.json()["result"]
        print("Got token:", self.token)

    def make_call(self, method, params):
        logging.info("________ Make Call ________")
        payload = {

            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 0,
            "auth": self.token
        }
        logging.info(payload)

        payload_json = json.dumps(payload)
        headers = {"Content-Type": "application/json-rpc"}
        r = requests.post(self.host, data=payload_json, headers=headers, verify=False)
        logging.info(r.json()['result'])

        return r.json()['result']


def get_host_list(groups_str, logfile):
    z = ZabbixService()

    logging.info("________ Get Host List ________")

    get_gid = lambda gname: z.make_call('hostgroup.get', {"filter": {"name": gname}, "output": ["groupid"]})

    groups = groups_str.split(",")
    group_ids = [get_gid(gname)[0]["groupid"] for gname in groups]

    print("group_ids :", group_ids)

    hosts = z.make_call('host.get', {"groupids": group_ids, "output": ["hostid", "host"]})
    logging.info(hosts)

    print("hosts :", hosts)

    with open(logfile, "w") as f:
        for item in hosts:
            f.write(item["host"])
            f.write("\n")

    return hosts

def is_pbi_service(srvname):
    bln = ''
    ## ==> curl -vvv -u prd-middleware-api -k https://data.api.intranatixis.com/transaction/supervision/v1/hostDetailshostname=SWDCFRQ30166
    endpoint = 'https://data.api.intranatixis.com/transaction/supervision/v1/hostDetailshostname=' + srvname
    print(endpoint)
    return bln

# pathFolder = "C:\\Users\\celerierma\\OneDrive - Groupe BPCE\\00-PROJETS\\04-PBI\\RIFA\\WorkInProgress"
# z_pbisrv = pathFolder + "\\logs\\zabbix_pbi_srv.txt"
# get_host_list('prd-middleware_powerbi_prod,prd-middleware_powerbi_horsprod', z_pbisrv)