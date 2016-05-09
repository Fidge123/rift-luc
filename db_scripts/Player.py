#!/usr/bin/env python3
"""Take match and player data, get champ and save it to the database"""

import json
import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def updateAttributes(match_id, player_id, region, match):
    conn_string = "host=" + HOST + " dbname=" + DBNAME + " user=" + USER + " password=" + PASS
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "SELECT wins,winstreak,losestreak,minion,wardkills,wardplaced,kills,deaths,assists,gold,largestkillingspree,csperminute,highestcrit,ccduration,teemowin FROM player WHERE id = %s AND region = %s;"
    data = (player_id, region)
    cursor.execute(query, data)
    attributes = cursor.fetchone()
    i = 0
    for attribute in attributes:
        if i == 0:
            if match["stats"]["win"]:
                win = attribute + 1
                query = "UPDATE player SET (wins) = ('" + str(win) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==1:
            if match["stats"]["win"]:
                winstreak = attribute + 1
            else:
                winstreak = 0
                query = "UPDATE player SET (winstreak) = ('" + str(winstreak) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==2:
            if match["stats"]["win"]:
                losestreak = 0
            else:
                losestreak = attribute + 1
                query = "UPDATE player SET (winstreak) = ('" + str(losestreak) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==3:
            if "minionsKilled" in match["stats"]:
                m = match["stats"]["minionsKilled"] + attribute
                query = "UPDATE player SET (minion) = ('" + str(m) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==4:
            if "wardKilled" in match["stats"]:
                w = match["stats"]["wardKilled"] + attribute
                query = "UPDATE player SET (wardkills) = ('" + str(w) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==5:
            if "wardPlaced" in match["stats"]:
                w = match["stats"]["wardPlaced"] + attribute
                query = "UPDATE player SET (wardplaced) = ('" + str(w) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==6:
            if "championsKilled" in match["stats"]:
                c = match["stats"]["championsKilled"] + attribute
                query = "UPDATE player SET (kills) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==7:
            if "numDeaths" in match["stats"]:
                c = match["stats"]["numDeaths"] + attribute
                query = "UPDATE player SET (deaths) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==8:
            if "assists" in match["stats"]:
                c = match["stats"]["assists"] + attribute
                query = "UPDATE player SET (assists) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==9:
            if "goldSpent" in match["stats"]:
                c = match["stats"]["goldSpent"] + attribute
                query = "UPDATE player SET (gold) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==10:
            if "largestKillingSpree" in match["stats"]:
                if attribute < match["stats"]["largestKillingSpree"]:
                    c = match["stats"]["largestKillingSpree"]
                    query = "UPDATE player SET (largestkillingspree) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                    data = (player_id, region)
                    cursor.execute(query,data)
                    conn.commit()
        elif i==11:
            if "csperminute" in match["stats"]:
                if attribute: 
                    c = match["stats"]["goldSpent"]
                    query = "UPDATE player SET (csperminute) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                    data = (player_id, region)
                    cursor.execute(query,data)
                    conn.commit()
        elif i==12:
            if "largestCriticalStrike" in match["stats"]:
                if attribute < match["stats"]["largestCriticalStrike"]:
                    c = match["stats"]["largestCriticalStrike"]
                    query = "UPDATE player SET (highestcrit) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                    data = (player_id, region)
                    cursor.execute(query,data)
                    conn.commit()
        elif i==13:
            if "totalTimeCrowdControlDealt" in match["stats"]:
                c = match["stats"]["totalTimeCrowdControlDealt"] + attribute
                query = "UPDATE player SET (ccduration) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                data = (player_id, region)
                cursor.execute(query,data)
                conn.commit()
        elif i==14:
            if match["championId"] == 17:
                if match["stats"]["win"]:
                    c = attribute + 1
                    query = "UPDATE player SET (teemowin) = ('" + str(c) + "') WHERE id = %s AND region =%s;"
                    data = (player_id, region)
                    cursor.execute(query,data)
                    conn.commit()
        i+=1
