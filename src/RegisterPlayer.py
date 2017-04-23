#!/usr/bin/env python3
"""Take player data and save it to the database"""

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

def register_player(name, region, password):
    """Main function"""
    name = name.lower()
    region = region.lower()
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = "INSERT INTO basic_auth.users(leaguename, region, pass, role) VALUES (%s,%s,%s,%s);"
    data = (name, region, password, "player")
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
