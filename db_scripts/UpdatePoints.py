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

R_SELECT = "SELECT id, points FROM repeatable;"
P_UPDATE = "UPDATE player SET points = points + %s WHERE id = %s;"
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

    for repeatable in repeatables:
        i = repeatable[0]
        stats = data["stats"]
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

def calculate_points(player_id, match_id, region, data):
    """Main function"""

    api = 'https://' + region + '.api.pvp.net/api/lol/' + region
    response = requests.get(api + '/v2.2/match/' + str(match_id), params=KEY)

    if response.status_code != 200:
        time.sleep(1)
        return calculate_points(player_id, match_id, region, data)

    game = json.loads(response.text)
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    calculate_repeatable(player_id, match_id, region, data, game, cursor)

    conn.commit()
    cursor.close()
    conn.close()
