#!/usr/bin/env python3
"""Take achievements and save it to the database"""

from os import environ
import json
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

with open("data/achievements.json") as file:
    ACHIEVEMENTS = json.load(file)

def fill_achievement_table():
    """Main function"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    
    for item in ACHIEVEMENTS:
        query = "SELECT name, description, points FROM achievement WHERE name = %s AND description = %s AND points = %s;"
        data = (item["name"], item["description"], item["points"])
        cursor.execute(query,data)
        if cursor.rowcount == 0:    #new achievement
            query = "INSERT INTO achievement(name, description, points) VALUES (%s,%s,%s);"
            cursor.execute(query, data)

    conn.commit()
    cursor.close()
    conn.close()
