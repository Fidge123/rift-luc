#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

CONN_STRING = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
CONN = psycopg2.connect(CONN_STRING)

def update(attribute, value, settings, cursor):
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
        minion = attributes["minion"] + match["stats"]["minionsKilled"]
        update("minion", minion, settings, cursor)

    if "wardKilled" in match["stats"]:
        wardkills = attributes["wardkills"] + match["stats"]["wardKilled"]
        update("wardkills", wardkills, settings, cursor)

    if "wardPlaced" in match["stats"]:
        wardplaced = attributes["wardplaced"] + match["stats"]["wardPlaced"]
        update("wardplaced", wardplaced, settings, cursor)

    if "championsKilled" in match["stats"]:
        kills = attributes["kills"] + match["stats"]["championsKilled"]
        update("kills", kills, settings, cursor)

    if "numDeaths" in match["stats"]:
        deaths = attributes["deaths"] + match["stats"]["numDeaths"]
        update("deaths", deaths, settings, cursor)

    if "assists" in match["stats"]:
        assists = attributes["assists"] + match["stats"]["assists"]
        update("assists", assists, settings, cursor)

    if "goldSpent" in match["stats"]:
        gold = attributes["gold"] + match["stats"]["goldSpent"]
        update("gold", gold, settings, cursor)

    if "largestKillingSpree" in match["stats"] and attributes["largestkillingspree"] < match["stats"]["largestKillingSpree"]:
        spree = match["stats"]["largestKillingSpree"]
        update("largestkillingspree", spree, settings, cursor)

    if "largestCriticalStrike" in match["stats"] and attributes["highestcrit"] < match["stats"]["largestCriticalStrike"]:
        crit = match["stats"]["largestCriticalStrike"]
        update("highestcrit", crit, settings, cursor)

    if "totalTimeCrowdControlDealt" in match["stats"]:
        duration = attributes["ccduration"] + match["stats"]["totalTimeCrowdControlDealt"]
        update("ccduration", duration, settings, cursor)

    if match["championId"] == 17:
        amount = attributes["teemoamount"] + 1
        update("teemoamount", amount, settings, cursor)

        if match["stats"]["win"]:
            win = attributes["teemowin"] + 1
            update("teemowin", win, settings, cursor)
