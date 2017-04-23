#!/usr/bin/env python3
"""Take argument"""

from sys import argv
from os import environ
from threading import Thread
import getopt
import psycopg2
import time
import GetRecentMatches
import Player
import RegisterPlayer
import FillAchievementTable
import UpdateChampionTable
import FillHallOfFameTable
import FillRepeatableTable

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

def usage():
    """Show usage help"""
    print("Schema: main.py --update\n" +
          "main.py --reset\n" +
          "main.py --register --name='name' --region='region' --password='password'\n" +
          "main.py --register -n 'name' -r 'region -p 'password'\n" +
          "main.py --verify")

def delete():
    """Delete tables"""
    conn = psycopg2.connect(CONN_STRING)
    cur = conn.cursor()
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE;")
    cur.execute("DROP SCHEMA IF EXISTS basic_auth CASCADE;")
    cur.execute("DROP ROLE IF EXISTS player")
    cur.execute("DROP ROLE IF EXISTS anon")
    cur.execute("CREATE SCHEMA public;")
    conn.commit()
    cur.close()
    conn.close()

def create():
    """Create tables"""
    conn = psycopg2.connect(CONN_STRING)
    with conn.cursor() as cursor:
        cursor.execute(open("db_scripts/DatabaseCreation.sql", "r").read())
    conn.commit()
    conn.close()

def fill(opts):
    """Fill data with static data"""
    region = 'euw'
    for opt, arg in opts[0]:
        if opt in ("-r", "--region"):
            region = arg.lower()
    FillAchievementTable.fill_achievement_table()
    UpdateChampionTable.update_champion_table(region)
    FillHallOfFameTable.fill_hall_of_fame_table()
    FillRepeatableTable.fill_repeatable_table()

def register(opts):
    """Register a new player"""
    name = region = password = ""

    for opt, arg in opts[0]:
        if opt in ("-n", "--name"):
            name = arg
        elif opt in ("-r", "--region"):
            region = arg
        elif opt in ("-p", "--password"):
            password = arg

    if name and region and password:
        RegisterPlayer.register_player(name, region, password)
    else:
        usage()

def update_loop():
    s_time = time.time()
    while True:
        print("UPDATING")
        GetRecentMatches.get_all_recent_matches()
        time.sleep(3600 - ((time.time() - s_time) % 3600))

def verify_loop():
    s_time = time.time()
    while True:
        print("VERIFYING")
        Player.copy_from_users()
        time.sleep(60 - ((time.time() - s_time) % 60))

def main():
    """Run requested command"""

    if len(argv) == 1:
        print("Please give an argument or use main.py -h/--help for options")

    try:
        opts = getopt.getopt(argv[1:], "hn:r:p:",
                             ["help", "update", "register", "verify",
                              "name=", "region=", "password=", "reset",
                              "start"])

        for opt in opts[0]:
            if opt[0] in ("-h", "--help"):
                usage()
            elif opt[0] == "--update":
                GetRecentMatches.get_all_recent_matches()
            elif opt[0] == "--register":
                register(opts)
            elif opt[0] == "--verify":
                Player.copy_from_users()
            elif opt[0] == "--reset":
                #delete()
                create()
                fill(opts)
            elif opt[0] == "--start":
                fill(opts)
                t1 = Thread(target=update_loop, daemon=False)
                t2 = Thread(target=verify_loop, daemon=False)
                t1.start()
                t2.start()

    except getopt.GetoptError as err:
        print(err)
        usage()

if __name__ == "__main__":
    main()
