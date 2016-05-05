#!/usr/bin/env python3
"""Request new game data and save it to the database"""

import json
import requests

with open('key') as file:
    KEY = {'api_key': file.readline().strip()}

YORDLES = ['Amumu', 'Corki', 'Gnar', 'Heimer', 'Lulu', 'Kennen', 'Poppy', 'Rumble', 'Teemo',
           'Tristana', 'Veigar', 'Ziggs']
STEALTH = ['Akali', 'Evelynn', 'Khazix', 'Rengar', 'LeBlanc', 'Shaco', 'Talon', 'Teemo', 'Twitch',
           'Vayne', 'Wukong']
VOID = ['Chogath', 'Kassadin', 'Khazix', 'KogMaw', 'Malzahar', 'RekSai', 'Velkoz']

def fill_champion_table(region):
    """Main function"""

    api = 'https://' + region + '.api.pvp.net/api/lol/' + region
    static = 'https://global.api.pvp.net/api/lol/static-data/' + region

    champs = json.loads(requests.get(api + '/v1.2/champion', params=KEY).text)['champions']
    s_champs = json.loads(requests.get(static + '/v1.2/champion', params=KEY).text)['data']

    champions = []
    names = []

    for name in s_champs:
        names.append(name)

    names.sort()

    for i, champ in enumerate(champs):
        name = names[i]
        champions.append({
            'name': name,
            'id': champ['id'],
            'f2p': champ['freeToPlay'],
            'yordle': name in YORDLES,
            'stealth': name in STEALTH,
            'void': name in VOID
        })
#conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
#conn = psycopg2.connect(conn_string)
