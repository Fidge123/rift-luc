#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

from os import environ
import json
import time
import psycopg2
import requests
import GetRecentMatches

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
CONN = psycopg2.connect(CONN_STRING)

def copy_from_users():
    """Create new player from (validated) user"""
    cursor = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT leaguename, region FROM basic_auth.users;"
    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        query = "SELECT id FROM player WHERE leaguename = %s AND region = %s;"
        cursor.execute(query, (user["leaguename"], user["region"]))
        if cursor.rowcount == 0:
            url = "https://" + user["region"] + ".api.pvp.net/api/lol/" + user["region"] + "/v1.4/summoner/by-name/" + user["leaguename"]
            response = requests.get(url, params=KEY)
            while response.status_code != 200:
                if response.status_code == 404:
                    return
                print(str(response.status_code) + ": Request failed, waiting 10 seconds")
                time.sleep(10)
                response = requests.get(url, params=KEY)
            player = json.loads(response.text)[user["leaguename"].lower().replace(" ", "")]
            query = "INSERT INTO player (id, leaguename, region, iconid, created) VALUES (%s,%s,%s,%s,%s);"
            timestamp = int(round(time.time()*1000))
            data = (player["id"], user["leaguename"], user["region"], player["profileIconId"], timestamp)
            cursor.execute(query, data)
            CONN.commit()
            GetRecentMatches.get_recent_matches(player["id"], user["region"], timestamp)

def update(attribute, value, settings, cursor):
    """Write data to table"""
    query = "UPDATE player SET (" + attribute + ") = (%s) WHERE id = %s AND region = %s;"
    data = (value, settings["player_id"], settings["region"])
    cursor.execute(query, data)
    CONN.commit()

def update_attributes(settings, match):
    """Update attributes for player"""
    cursor = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM player WHERE id = %s AND region = %s;"
    data = (settings["player_id"], settings["region"])
    cursor.execute(query, data)
    attributes = cursor.fetchone()

    if match["stats"]["win"]:
        win = attributes["wins"] + 1
        winstreak = attributes["winstreak"] + 1
        losestreak = 0

        query = "UPDATE player SET (wins, winstreak, losestreak) = (%s,%s,%s) WHERE id = %s AND region = %s;"
        data = (win, winstreak, losestreak, settings["player_id"], settings["region"])
        cursor.execute(query, data)
        CONN.commit()
    else:
        winstreak = 0
        losestreak = attributes["losestreak"] + 1

        query = "UPDATE player SET (winstreak, losestreak) = (%s,%s) WHERE id = %s AND region = %s;"
        data = (winstreak, losestreak, settings["player_id"], settings["region"])
        cursor.execute(query, data)
        CONN.commit()

    if "minionsKilled" in match["stats"]:
        update("minion", attributes["minion"] + match["stats"]["minionsKilled"], settings, cursor)

    if "wardKilled" in match["stats"]:
        update("wardkills", attributes["wardkills"] + match["stats"]["wardKilled"], settings, cursor)

    if "wardPlaced" in match["stats"]:
        update("wardplaced", attributes["wardplaced"] + match["stats"]["wardPlaced"], settings, cursor)

    if "championsKilled" in match["stats"]:
        update("kills", attributes["kills"] + match["stats"]["championsKilled"], settings, cursor)

    if "numDeaths" in match["stats"]:
        update("deaths", attributes["deaths"] + match["stats"]["numDeaths"], settings, cursor)

    if "assists" in match["stats"]:
        update("assists", attributes["assists"] + match["stats"]["assists"], settings, cursor)

    if "goldSpent" in match["stats"]:
        update("gold", attributes["gold"] + match["stats"]["goldSpent"], settings, cursor)

    if "largestKillingSpree" in match["stats"] and attributes["largestkillingspree"] < match["stats"]["largestKillingSpree"]:
        update("largestkillingspree", match["stats"]["largestKillingSpree"], settings, cursor)

    if "largestCriticalStrike" in match["stats"] and attributes["highestcrit"] < match["stats"]["largestCriticalStrike"]:
        update("highestcrit", match["stats"]["largestCriticalStrike"], settings, cursor)

    if "totalTimeCrowdControlDealt" in match["stats"]:
        update("ccduration", attributes["ccduration"] + match["stats"]["totalTimeCrowdControlDealt"], settings, cursor)

    if match["championId"] == 17:
        update("teemoamount", attributes["teemoamount"] + 1, settings, cursor)

        if match["stats"]["win"]:
            update("teemowin", attributes["teemowin"] + 1, settings, cursor)
