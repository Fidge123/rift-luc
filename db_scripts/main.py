#!/usr/bin/env python3
"""Take argument"""

from sys import argv
import getopt
import psycopg2
import GetRecentMatches
import RegisterPlayer
import FillAchievementTable, FillChampionTable, FillHallOfFameTable, FillRepeatableTable

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def usage():
    """Show usage help"""
    print("Schema: main.py --update \n" +
          "main.py --reset --region='region/-r 'region' \n" +
          "main.py --register --name='name' --region='region' " +
          "--emai='email' --password='password' --leagueid='leagueid' \n" +
          "main.py --register -n 'name' -r 'region -e 'email' -p 'password' " +
          "-l 'leagueid'")

def delete():
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    query = "DROP SCHEMA public CASCADE;"
    cur.execute(query)
    query = "CREATE SCHEMA public;"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def create():
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    with conn.cursor() as cursor:
        cursor.execute(open("DatabaseCreation.sql", "r").read())
    conn.commit()
    conn.close()

def fill(opts):
    region = 'euw'
    for opt, arg in opts[0]:
        if opt in ("-r", "--region"):
            region = arg
    if not region:
        usage()
        return
    FillAchievementTable.fill_achievement_table()
    FillChampionTable.fill_champion_table(region)
    FillHallOfFameTable.fill_hall_of_fame_table()
    FillRepeatableTable.fill_repeatable_table()

def register(opts):
    """Register a new player"""
    name = region = email = password = leagueid = ''

    for opt, arg in opts[0]:
        if opt in ("-n", "--name"):
            name = arg
        elif opt in ("-r", "--region"):
            region = arg
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-l", "--leagueid"):
            leagueid = arg

    if name and region and password and leagueid and email:
        RegisterPlayer.register_player(name, region, email, password, leagueid)
    else:
        usage()

def main():
    """Run requested command"""

    if len(argv) == 1:
        print("Please give an argument or use main.py -h/--help for options")

    try:
        opts = getopt.getopt(argv[1:], "hn:r:e:p:l:",
                             ["help", "update", "register", "name=", "region=",
                              "email=", "password=", "leagueid=", "reset"])

        for opt in opts[0]:
            if opt[0] in ("-h", "--help"):
                usage()
            elif opt[0] == "--update":
                GetRecentMatches.get_all_recent_matches()
            elif opt[0] == "--register":
                register(opts)
            elif opt[0] == "--reset":
                delete()
                create()
                fill(opts)
                

    except getopt.GetoptError as err:
        print(err)
        usage()

if __name__ == '__main__':
    main()
