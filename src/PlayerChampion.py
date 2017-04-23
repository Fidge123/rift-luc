#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

from os import environ
import psycopg2

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

def update(settings, match):
    """Update player champion table"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()

    query = "SELECT amount FROM player_champion WHERE playerid = %s AND region = %s AND championid = %s;"
    data = (settings["player_id"], settings["region"], match["championId"])
    cursor.execute(query, data)

    if cursor.rowcount == 0:
        query = "INSERT INTO player_champion(playerid,region,championid,amount) VALUES (%s,%s,%s,%s);"
        data = (settings["player_id"], settings["region"], match["championId"], 1)
        cursor.execute(query, data)
        conn.commit()
    else:
        amount = cursor.fetchone()[0] + 1
        query = "UPDATE player_champion SET (amount) = (%s) WHERE playerid = %s AND region = %s AND championid = %s;"
        data = (amount, settings["player_id"], settings["region"], match["championId"])
        cursor.execute(query, data)
        conn.commit()

    cursor.close()
    conn.close()
