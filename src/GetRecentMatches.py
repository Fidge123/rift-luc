#!/usr/bin/env python3
"""Take player data, request matches and save it to the database"""

from os import environ
import json
import time
import psycopg2
import requests
import PlayerChampion
import UpdatePoints
import Player
import UpdateHallOfFame

with open("key") as file:
    KEY = {"api_key": file.readline().strip()}

# with open("db_config") as file:
#     HOST = file.readline().strip()
#     DBNAME = file.readline().strip()
#     USER = file.readline().strip()
#     PASS = file.readline().strip()
#
# CONN_STRING = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS

CONN_STRING = environ["DATABASE_URL"]
# local way
# "host=" + environ['HOST'] + " dbname=" + environ['DBNAME'] + " user=" + environ['USER'] + " password=" + environ['PW']

def get_all_recent_matches():
    """Get recent matches for all players"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = "SELECT id, region, created FROM player;"
    cursor.execute(query)
    players = cursor.fetchall()

    for player in players:
        player_id = player[0]
        region = player[1]
        created = player[2]
        get_recent_matches(player_id, region, created)

def get_recent_matches(player_id, region, created):
    """Retrieve all matches that are not yet in the database for a given player id"""
    api = "https://" + region + ".api.pvp.net/api/lol/" + region
    response = requests.get(api + "/v1.3/game/by-summoner/" + str(player_id) + "/recent", params=KEY)

    while response.status_code != 200:
        if response.status_code == 404:
            return
        print(str(response.status_code) + ": Request failed, waiting 10 seconds")
        time.sleep(10)
        response = requests.get(api + "/v1.3/game/by-summoner/" + str(player_id) + "/recent", params=KEY)

    matches = json.loads(response.text)["games"]

    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()

    for match in matches:
        match_id = match["gameId"]
        settings = {
            "match_id": match_id,
            "player_id": player_id,
            "region": region,
            "created": created
        }
        query = "SELECT id, playerid, region FROM game WHERE id = %s AND playerid = %s AND region = %s;"
        cursor.execute(query, (match_id, player_id, region))

        if cursor.rowcount == 0 and created < match["createDate"]: #new match found
            query = "INSERT INTO game(id, playerid, region, created, json) VALUES (%s,%s,%s,%s,%s);"
            data = (match_id, player_id, region, created, json.dumps(match))
            cursor.execute(query, data)
            conn.commit()

            PlayerChampion.update(settings, match)
            Player.update_attributes(settings, match)
            UpdateHallOfFame.update()
            UpdatePoints.calculate_points(settings, match)

    cursor.close()
    conn.close()
