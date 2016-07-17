#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

HOF_INSERT = "INSERT INTO player_halloffame(playerid,region,hofid,place) VALUES (%s,%s,%s,%s);"

def update():
    """Update Hall of Fame data"""
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "DELETE FROM player_halloffame WHERE 1=1;"
    cursor.execute(query)
    conn.commit()
    for i in range(1, 9):
        if i == 1:
            query = "SELECT id, region, ((kills + assists) / GREATEST(deaths, 1) * 1.0) AS kda FROM player ORDER BY kda DESC LIMIT 3;"
        elif i == 2:
            query = "SELECT id, region FROM player ORDER BY assists DESC LIMIT 3;"
        elif i == 3:
            query = "SELECT id, region FROM player ORDER BY kills DESC LIMIT 3;"
        elif i == 4:
            continue
        elif i == 5:
            query = "SELECT id, region FROM player ORDER BY minion DESC LIMIT 3;"
        elif i == 6:
            continue
        elif i == 7:
            query = "SELECT id, region FROM player ORDER BY highestcrit DESC LIMIT 3;"
        elif i == 8:
            query = "SELECT id, region FROM player ORDER BY ccduration DESC LIMIT 3;"
        cursor.execute(query)
        result = cursor.fetchall()
        place = 1

        for player in result:
            player_id = player[0]
            region = player[1]
            data = (player_id, region, i, place)
            cursor.execute(HOF_INSERT, data)
            place += 1
