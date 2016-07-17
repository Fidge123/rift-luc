#!/usr/bin/env python3
"""Take HallOfFame and save it to the database"""

import json
import psycopg2

with open("db_config") as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

CONN_STRING = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS

with open("data/hall_of_fame.json") as file:
    HOF = json.load(file)

def fill_hall_of_fame_table():
    """Main function"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = "INSERT INTO halloffame(name, description, pointsfirst, pointssecond, pointsthird) VALUES (%s,%s,%s,%s,%s);"

    for item in HOF:
        data = (item["description"], item["description"], item["firstPlace"], item["secondPlace"], item["thirdPlace"])
        cursor.execute(query, data)

    conn.commit()
    cursor.close()
    conn.close()
