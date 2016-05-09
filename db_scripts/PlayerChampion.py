#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

import json
import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def update(match_id, player_id, region, match):
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    query = "SELECT amount FROM player_champion WHERE playerid = %s AND region = %s AND championid = %s;"
    data = (player_id, region, match["championId"])
    cursor.execute(query, data)
   
    if cursor.rowcount == 0:
        query = "INSERT INTO player_champion(playerid,region,championid,amount) VALUES (%s,%s,%s,%s);"
        data = (player_id, region, match["championId"], 1)
        cursor.execute(query, data)
        conn.commit()
    else:
        amount = cursor.fetchone()[0] + 1
        query = "UPDATE player_champion SET (amount) = (%s);"
        data = (amount,)
        cursor.execute(query, data)
        conn.commit()
        
    cursor.close()
    conn.close()
