#!/usr/bin/env python3
"""Take HallOfFame and save it to the database"""

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

CONN_STRING = "host=" + environ['HOST'] + " dbname=" + environ['DBNAME'] + " user=" + environ['USER'] + " password=" + environ['PW']

with open("data/hall_of_fame.json") as file:
    HOF = json.load(file)

def fill_hall_of_fame_table():
    """Main function"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    
    for item in HOF:
        query = "SELECT name, description FROM halloffame WHERE name = %s AND description = %s;"
        data = (item["description"], item["description"])
        cursor.execute(query,data)
        if cursor.rowcount == 0:
            data = (item["description"], item["description"], item["firstPlace"], item["secondPlace"], item["thirdPlace"])
            query = "INSERT INTO halloffame(name, description, pointsfirst, pointssecond, pointsthird) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(query, data)

    conn.commit()
    cursor.close()
    conn.close()
