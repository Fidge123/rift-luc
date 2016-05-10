#!/usr/bin/env python3
"""Take player data, request matches and save it to the database"""

import json
import time
import psycopg2
import requests
import PlayerChampion
import UpdatePoints
import Player

with open('key') as file:
    KEY = {'api_key': file.readline().strip()}

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def get_all_recent_matches():
    """Get recent matches for all players"""
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "SELECT id, region FROM player;"
    cursor.execute(query)
    players = cursor.fetchall()

    for player in players:
        player_id = player[0]
        region = player[1]
        get_recent_matches(player_id, region)

def get_recent_matches(player_id, region):
    """Retrieve all matches that are not yet in the database for a given player id"""
    api = 'https://' + region + '.api.pvp.net/api/lol/' + region
    response = requests.get(api + '/v1.3/game/by-summoner/' + str(player_id) + '/recent', params=KEY)

    while response.status_code != 200:
        if response.status_code == 404:
            return
        print(str(response.status_code) + ": Request failed, waiting 10 seconds")
        time.sleep(10)
        response = requests.get(api + '/v1.3/game/by-summoner/' + str(player_id) + '/recent', params=KEY)

    matches = json.loads(response.text)["games"]

    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    for match in matches:
        match_id = match["gameId"]
        query = "SELECT id, playerid, region FROM game WHERE id ='" + str(match_id) + "' AND playerid = '" + str(player_id) + "' AND region = '" + region + "';"
        cursor.execute(query)

        if cursor.rowcount == 0: #new match found
            query = "INSERT INTO game(id, playerid, region, json) VALUES (%s,%s,%s,%s);"
            data = (match_id, player_id, region, json.dumps(match))
            cursor.execute(query, data)
            conn.commit()

            PlayerChampion.update(match_id, player_id, region, match)
            Player.updateAttributes(match_id, player_id, region, match)
            UpdatePoints.calculate_points(player_id, match_id, region, match)

    cursor.close()
    conn.close()
