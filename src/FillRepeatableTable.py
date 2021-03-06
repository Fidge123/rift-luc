#!/usr/bin/env python3
"""Take repeatables and save it to the database"""

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

with open("data/repeatables.json") as file:
    REPEATABLES = json.load(file)

def fill_repeatable_table():
    """Main function"""
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    
    for item in REPEATABLES:
        query = "SELECT name, description, points FROM repeatable WHERE name = %s AND description = %s AND points = %s;"
        data = (item["description"], item["description"], item["points"])
        cursor.execute(query,data)
        if cursor.rowcount == 0:
            query = "INSERT INTO repeatable(name, description, points) VALUES (%s,%s,%s);"
            cursor.execute(query, data)

    conn.commit()
    cursor.close()
    conn.close()
