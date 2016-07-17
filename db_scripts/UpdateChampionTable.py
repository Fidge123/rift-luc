#!/usr/bin/env python3
"""Request new game data and updates the champion table"""

import json
import requests
import psycopg2

with open("key") as file:
    KEY = {"api_key": file.readline().strip()}

with open("db_config") as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

CONN_STRING = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS

# Also in FillChampionTable.py
YORDLES = ["Amumu", "Corki", "Gnar", "Heimer", "Lulu", "Kennen", "Poppy", "Rumble", "Teemo",
           "Tristana", "Veigar", "Ziggs"]
STEALTH = ["Akali", "Evelynn", "Khazix", "Rengar", "LeBlanc", "Shaco", "Talon", "Teemo", "Twitch",
           "Vayne", "Wukong"]
VOID = ["Chogath", "Kassadin", "Khazix", "KogMaw", "Malzahar", "RekSai", "Velkoz"]

def get_champions(region):
    """Get and combine champion data from API"""
    api = "https://" + region + ".api.pvp.net/api/lol/" + region
    static = "https://global.api.pvp.net/api/lol/static-data/" + region

    champs = json.loads(requests.get(api + "/v1.2/champion", params=KEY).text)["champions"]
    s_champs = json.loads(requests.get(static + "/v1.2/champion", params=KEY).text)["data"]

    champions = []
    names = []

    for name in s_champs:
        names.append(name)

    names.sort()

    for i, champ in enumerate(champs):
        name = names[i]
        champions.append({
            "name": name,
            "id": champ["id"],
            "f2p": champ["freeToPlay"],
            "yordle": name in YORDLES,
            "stealth": name in STEALTH,
            "void": name in VOID
        })

    return champions

def update_champion_table(region):
    """Main function"""
    champions = get_champions(region)

    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = "SELECT name FROM champion;"
    cursor.execute(query)
    db_champs = cursor.fetchall()

    for champ in champions:
        query = "SELECT ftp FROM champion WHERE id = %s;"
        cursor.execute(query, (champ["id"],))
        champ2 = cursor.fetchone()

        if (champ["name"],) not in db_champs:  #new champion
            query = "INSERT INTO champion(id,name,ftp,yordle,stealth,void) VAlUES (%s,%s,%s,%s,%s,%s);"
            data = (champ["id"], champ["name"], champ["f2p"],
                    champ["yordle"], champ["stealth"], champ["void"])
            cursor.execute(query, data)
            conn.commit()

        if (champ["f2p"],) != champ2:  #new f2p rotation
            query = "UPDATE champion SET (ftp) = (%s) WHERE id = %s;"
            cursor.execute(query, (champ["f2p"], champ["id"]))
            conn.commit()

    cursor.close()
    conn.close()
