#!/usr/bin/env python3
"""Take player data, request matches and save it to the database"""

import json
import psycopg2
import requests

with open('key') as file:
    KEY = {'api_key': file.readline().strip()}

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def get_recent_matches(player_id, region):

    api = 'https://' + region + '.api.pvp.net/api/lol/' + region

    matches = json.loads(requests.get(api + '/v1.3/game/by-summoner/' + player_id + '/recent', params=KEY).text)["games"]
    
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
    for match in matches:
        match_id = match["gameId"]
        query = "SELECT id, playerid, region FROM game WHERE id ='" + str(match_id) + "' AND playerid = '" + player_id + "' AND region = '" + region + "';"
        cursor.execute(query)
        if cursor.rowcount == 0: #new match found
            query = "INSERT INTO game(id, playerid, region, json) VALUES (%s,%s,%s,%s);"
            data = (match_id, player_id, region, str(match))
            cursor.execute(query, data)
            conn.commit()

    cursor.close()
    conn.close()
