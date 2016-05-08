#!/usr/bin/env python3
"""Take achievements and save it to the database"""

import json
import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

with open('data/achievements.json') as file:
    ACHIEVEMENTS = json.load(file)

def fill_achievement_table():
    """Main function"""

    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "INSERT INTO achievement(name, description, points) VALUES (%s,%s,%s);"

    for item in ACHIEVEMENTS:
        data = (item["name"], item["description"], item["points"])
        cursor.execute(query, data)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    fill_achievement_table()
