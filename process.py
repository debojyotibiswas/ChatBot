import re
import requests
import json

def process_ip(inp):
    Pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    ip_list = re.findall(Pattern,inp)
    return ip_list

def process_status1(inp):
    inp = inp.rstrip()
    with open("ServerList.json") as file:
        data = json.load(file)
    for dics in data['servers']:
        if inp in dics['name'].lower():
            for servers,urls in dics['urls'].items():
                print(servers)
                print(urls)
                #r = request.get(urls[0],timeout=5,verify = False)
                #print(r.status_code)

def process_status2(inp):
    with open("ServerList.json") as file:
        data = json.load(file)
    for dics in data['servers']:
        if dics['name'].lower() in inp:
            for servers,urls in dics['urls'].items():
                if dics['name'].lower() + ' ' + servers.lower() == inp:
                    print(urls[0])
                    #r = request.get(urls[0],timeout=5,verify = False)
                    #print(r.status_code)


def process_status3(inp):
    with open("ServerList.json") as file:
        data = json.load(file)
    for dics in data['servers']:
        for servers,urls in dics['urls'].items():
            if urls[1] == inp:
                print(urls[0])
                #r = request.get(urls[0],timeout=5,verify = False)
                #print(r.status_code)
