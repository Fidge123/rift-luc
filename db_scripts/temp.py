#!/usr/bin/env python3
"""Request new game data and save it to the database"""

import json
import requests

with open('key') as f:
    KEY = {'api_key': f.read().splitlines()[0]}

REGION = 'euw'
API = 'https://' + REGION + '.api.pvp.net/api/lol/' + REGION
CHAMPS = json.loads(requests.get(API + '/v1.2/champion', params=KEY).text)['champions']
S_CHAMPS = json.loads(requests.get('https://global.api.pvp.net/api/lol/static-data/' + REGION + '/v1.2/champion',
                                   params=KEY).text)['data']
championId = []
championFtp = []
championYordle = []
championStealth = []
championVoid = []
championName = []
YORDLES = ['Amumu', 'Corki', 'Gnar', 'Heimer', 'Lulu', 'Kennen', 'Poppy',
           'Rumble', 'Teemo', 'Tristana', 'Veigar', 'Ziggs']
STEALTH = ['Akali', 'Evelynn', 'Khazix', 'Rengar', 'LeBlanc', 'Shaco',
           'Talon', 'Teemo', 'Twitch', 'Vayne', 'Wukong']
VOID = ['Chogath', 'Kassadin', 'Khazix', 'KogMaw', 'Malzahar', 'RekSai', 'Velkoz']

for name in S_CHAMPS:
    championName.append(name)

championName.sort()

for i, champ in enumerate(CHAMPS):
    championId.append(champ['id'])
    championFtp.append(champ['freeToPlay'])
    championYordle.append(championName[i] in YORDLES)
    championStealth.append(championName[i] in STEALTH)
    championVoid.append(championName[i] in VOID)

#conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
#conn = psycopg2.connect(conn_string)
