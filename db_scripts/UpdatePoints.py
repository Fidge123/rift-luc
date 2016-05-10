#!/usr/bin/env python3
"""Calculate points for a certain game and player"""
import json
import time
import psycopg2
import requests

with open('key') as file:
    KEY = {'api_key': file.readline().strip()}

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

### Common queries ###
P_UPDATE = "UPDATE player SET points = points + %s WHERE id = %s;"

### Repeatables ###
R_SELECT = "SELECT id, points FROM repeatable;"
PR_SELECT = "SELECT amount FROM player_repeatable WHERE playerid = %s AND region = %s AND repeatableid = %s;"
PR_INSERT = "INSERT INTO player_repeatable(amount, playerid, region, repeatableid) VALUES (%s,%s,%s,%s);"
PR_UPDATE = "UPDATE player_repeatable SET amount = amount + %s WHERE playerid = %s AND region = %s AND repeatableid = %s;"
GRP_INSERT = "INSERT INTO game_repeatable_player(playerid, region, repeatableid, gameid) VALUES (%s,%s,%s,%s);"

def update_repeatable_tables(cursor, player_id, match_id, region, repeatable_id, points):
    """Update database with repeatable points"""
    cursor.execute(P_UPDATE, (points, player_id))
    cursor.execute(GRP_INSERT, (player_id, region, repeatable_id, match_id))

    cursor.execute(PR_SELECT, (player_id, region, repeatable_id))
    if cursor.rowcount == 0:
        cursor.execute(PR_INSERT, (1, player_id, region, repeatable_id))
    else:
        cursor.execute(PR_UPDATE, (1, player_id, region, repeatable_id))

def dealt_highest_damage(damage, participants):
    """Check if player dealt most damage"""
    highest = damage

    for participant in participants:
        highest = max(highest, participant["stats"]["totalDamageDealtToChampions"])

    return highest == damage

def kda_greater_than(limit, stats):
    if "numDeaths" in stats:
        if stats["numDeaths"] == 0:
            stats["numDeaths"] = 1
        if (stats.get("assists", 0) + stats.get("championsKilled", 0)) / stats["numDeaths"] > limit:
            return True
    return False

def stole_ten_monster(champ_id, team_id, participants):
    """Check if player stole 10 jungle creeps"""
    for participant in participants:
        if (participant["teamId"] == team_id
                and participant["championId"] == champ_id
                and participant["stats"].get("neutralMinionsKilledEnemyJungle", 0) > 10):
            return True
    return False

def killed_baron(team_id, teams):
    """Check if team killed baron"""
    for team in teams:
        if team["teamId"] == team_id and team.get("baronKills", 0) > 0:
            return True
    return False

def killed_vilemaw(team_id, teams):
    """Check if team killed vilemaw"""
    for team in teams:
        if team["teamId"] == team_id and team.get("vilemawKills", 0) > 0:
            return True
    return False

def calculate_repeatable(player_id, match_id, region, data, game, cursor):
    """Calculate repeatables"""

    cursor.execute(R_SELECT)
    repeatables = cursor.fetchall()
    stats = data["stats"]

    for repeatable in repeatables:
        i = repeatable[0]
        if (i == 1 and stats["win"] or
                i == 2 and stats.get("championsKilled", 0) >= 10 or
                i == 3 and stats.get("largestMultiKill", 0) == 3 or
                i == 4 and stats.get("largestMultiKill", 0) == 4 or
                i == 5 and stats.get("largestMultiKill", 0) == 5 or
                i == 6 and stats.get("assists", 0) >= 10 or
                i == 7 and stats.get("minionsKilled", 0) >= 300 or
                i == 8 and stats.get("minionsKilled", 0) >= 400 or
                i == 9 and stats.get("minionsKilled", 0) >= 500 or
                i == 10 and dealt_highest_damage(stats.get("totalDamageDealtToChampions", 0), game.get("participants", [])) or
                i == 11 and kda_greater_than(10, stats) or
                i == 12 and kda_greater_than(20, stats) or
                i == 13 and stats["win"] and stats.get("numDeaths", 1) == 0 or
                i == 14 and stole_ten_monster(data["championId"], data["teamId"], game.get("participants", [])) or
                i == 15 and killed_baron(data["teamId"], game["teams"]) or
                i == 16 and killed_vilemaw(data["teamId"], game["teams"])):
            update_repeatable_tables(cursor, player_id, match_id, region, i, repeatable[1])

### Achievements ###
A_SELECT = "SELECT id, points FROM achievement;"
P_SELECT = "SELECT wins,minion,assists,wardplaced,wardkills,winstreak,losestreak,gold,largestkillingspree,stealthamount,voidamount,yordleamount,teemowin,teemoamount FROM player WHERE id = %s;"
PAM_SELECT = "SELECT gameid FROM player_achievement_match WHERE playerid = %s AND region = %s AND achievementid = %s;"
PAM_INSERT = "INSERT INTO player_achievement_match(playerid, region, achievementid, gameid) VALUES (%s,%s,%s,%s);"
CHAMP_COUNT = "SELECT COUNT(championid) FROM player_champion WHERE playerid=%s;"
YORDLE_SELECT = "SELECT COUNT(c.id) FROM champion AS c, player_champion AS pc WHERE yordle=TRUE AND c.id=pc.championid AND pc.playerid=%s;"
STEALTH_SELECT = "SELECT COUNT(c.id) FROM champion AS c, player_champion AS pc WHERE stealth=TRUE AND c.id=pc.championid AND pc.playerid=%s;"
VOID_SELECT = "SELECT COUNT(c.id) FROM champion AS c, player_champion AS pc WHERE void=TRUE AND c.id=pc.championid AND pc.playerid=%s;"
F2P_SELECT = "SELECT COUNT(c.id) FROM champion AS c, player_champion AS pc WHERE ftp=TRUE AND c.id=pc.championid AND pc.playerid=%s;"

def three_yordles(player_id, cursor):
    """Check if player used at least 3 different yordles"""
    cursor.execute(YORDLE_SELECT, (player_id,))
    return cursor.fetchone()[0] >= 3

def three_stealth(player_id, cursor):
    """Check if player used at least 3 different stealth champs"""
    cursor.execute(STEALTH_SELECT, (player_id,))
    return cursor.fetchone()[0] >= 3

def three_void(player_id, cursor):
    """Check if player used at least 3 different void champs"""
    cursor.execute(VOID_SELECT, (player_id,))
    return cursor.fetchone()[0] >= 3

def free_to_play(player_id, cursor):
    """Check if player used at least 10 champions that are free to play"""
    cursor.execute(F2P_SELECT, (player_id,))
    return cursor.fetchone()[0] >= 10

def update_achievement_tables(player_id, match_id, region, achievement_id, cursor):
    """Insert achievement into table if it doesnt exist yet"""
    cursor.execute(PAM_SELECT, (player_id, region, achievement_id))
    if cursor.rowcount == 0:
        cursor.execute(PAM_INSERT, (player_id, region, achievement_id, match_id))

def calculate_achievements(player_id, match_id, region, data, game, cursor):
    """Calculate achievements"""
    cursor.execute(P_SELECT, (player_id,))
    player = cursor.fetchone()
    cursor.execute(CHAMP_COUNT, (player_id,))
    champ_pool = cursor.fetchone()[0]
    cursor.execute(A_SELECT)
    achievements = cursor.fetchall()
    stats = data["stats"]
    funmodes = ["ODIN", "ONEFORALL", "ASCENSION", "FIRSTBLOOD", "KINGPORO"]

    for achievement in achievements:
        i = achievement[0]
        if (i == 1 and player[11] >= 3 or # yordleamount
                i == 2 and three_yordles(player_id, cursor) or
                i == 3 and player[0] > 0 or # wins
                i == 4 and player[0] >= 10 or
                i == 5 and player[0] >= 20 or
                i == 6 and player[0] >= 30 or
                i == 7 and champ_pool > 10 or
                i == 8 and champ_pool > 20 or
                i == 9 and champ_pool > 30 or
                i == 10 and player[1] > 3000 or # cs
                i == 11 and player[1] > 4000 or
                i == 12 and player[1] > 5000 or
                i == 13 and player[2] > 100 or # assists
                i == 14 and player[2] > 200 or
                i == 15 and player[2] > 300 or
                i == 16 and player[3] > 100 or # wardplaced
                i == 17 and player[3] > 200 or
                i == 18 and player[3] > 300 or
                i == 19 and player[3] > 500 or
                i == 20 and player[4] > 50 or # wardkills
                i == 21 and player[4] > 100 or
                i == 22 and player[4] > 200 or
                i == 23 and player[5] > 6 or # winstreak
                i == 24 and player[5] > 8 or
                i == 25 and player[5] > 10 or
                i == 26 and player[6] > 5 or # losestreak
                i == 27 and game.get("matchDuration", 1500) < 1230 or
                i == 28 and False or
                i == 29 and stats["win"] and data.get("subType", "") == "NORMAL" or
                i == 30 and stats["win"] and data.get("subType", "") == "NORMAL_3x3" or
                i == 31 and stats["win"] and data.get("subType", "") == "ARAM_UNRANKED_5x5" or
                i == 32 and stats["win"] and data.get("gameMode", "") in funmodes or
                i == 33 and False or
                i == 34 and data.get("gameMode", "") == "TUTORIAL" or
                i == 35 and False or
                i == 36 and player[7] > 1000000 or # gold
                i == 37 and player[8] > 4 or # largestkillingspree
                i == 38 and player[8] > 8 or
                i == 39 and player[8] > 12 or
                i == 40 and data.get("spell1", 4) != 4 and data.get("spell2", 4) != 4 or
                i == 41 and game.get("matchDuration", 1500) < 3600 or
                i == 42 and player[9] >= 3 or #stealth
                i == 43 and three_stealth(player_id, cursor) or
                i == 44 and player[10] >= 3 or # void
                i == 45 and three_void(player_id, cursor) or
                i == 46 and player[12] == 1 or # teemowin
                i == 47 and player[12] == 2 or
                i == 48 and player[12] == 3 or
                i == 49 and player[13] == 2 or # teemoamount
                i == 50 and player[13] == 3 or
                i == 51 and player[13] == 4 or
                i == 52 and False or
                i == 53 and free_to_play(player_id, cursor)):
            update_achievement_tables(player_id, match_id, region, i, cursor)

def calculate_points(player_id, match_id, region, data):
    """Main function"""

    api = 'https://' + region + '.api.pvp.net/api/lol/' + region
    response = requests.get(api + '/v2.2/match/' + str(match_id), params=KEY)

    while response.status_code != 200:
        if response.status_code == 404:
            return
        print(str(response.status_code) + ": Request failed, waiting 10 seconds")
        time.sleep(10)
        response = requests.get(api + '/v2.2/match/' + str(match_id), params=KEY)

    game = json.loads(response.text)
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    calculate_repeatable(player_id, match_id, region, data, game, cursor)
    conn.commit()
    calculate_achievements(player_id, match_id, region, data, game, cursor)
    conn.commit()

    cursor.close()
    conn.close()
