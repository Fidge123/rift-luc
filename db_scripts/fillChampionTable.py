import requests
import json
#import psycopg2

key_file = open('key')
key = key_file.readline()
payload = {'api_key': key}
r = requests.get('https://euw.api.pvp.net/api/lol/euw/v1.2/champion', params=payload)
champion_json = json.loads(r.text)
length = len(champion_json['champions'])
champion_id = []
champion_ftp = []
champion_yordle = []
champion_stealth = []
champion_void = []
champion_name = []
yordles = ['Amumu', 'Corki', 'Gnar', 'Heimer', 'Lulu', 'Kennen', 'Poppy', 'Rumble', 'Teemo', 'Tristana', 'Veigar', 'Ziggs']
stealth = ['Akali', 'Evelynn', 'Khazix', 'Rengar', 'LeBlanc', 'Shaco', 'Talon', 'Teemo', 'Twitch', 'Vayne', 'Wukong']
void = ['Chogath', 'Kassadin', 'Khazix', 'KogMaw', 'Malzahar', 'RekSai' ,'Velkoz']
r2=requests.get('https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion', params=payload)
for name in json.loads(r2.text)['data']:
    champion_name.append(name)
champion_name.sort()
for x in range(0, length):
    champion_id.append(champion_json['champions'][x]['id'])
    champion_ftp.append(champion_json['champions'][x]['freeToPlay'])
    if(champion_name[x] in yordles):
        champion_yordle.append(True)
    else:
        champion_yordle.append(False)
    if(champion_name[x] in stealth):
        champion_stealth.append(True)
    else:
        champion_stealth.append(False)
    if(champion_name[x] in void):
        champion_void.append(True)
    else:
        champion_void.append(False)
#conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
#conn = psycopg2.connect(conn_string)
