#!/usr/bin/env python3
"""Take player data and save it to the database"""

import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def register_player(name, region, password):
    """Main function"""

    region = region.lower()
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "INSERT INTO basic_auth.users(leaguename, region, pass, role) VALUES (%s,%s,%s,%s);"
    data = (name, region, password, 'player')
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
