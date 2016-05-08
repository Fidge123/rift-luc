#!/usr/bin/env python3
"""Take achievements and save it to the database"""

import psycopg2

with open('db_config') as file:
    HOST = file.readline().strip()
    DBNAME = file.readline().strip()
    USER = file.readline().strip()
    PASS = file.readline().strip()

def fill_achievement_table():
    """Main function"""

    description = ['Play 3 yordles', 'Play 3 different yordles', 'Win a game',
                   'Win 10 games', 'Win 20 games', 'Win 30 games', 'Win with 10 different chamos',
                   'Win with 20 different champs', 'Win with 30 different champs',
                   'Kill 3000 minions', 'Kill 400 minions', 'Kill 5000 minions',
                   'Get 100 assists', 'Get 200 assists', 'Get 300 assists',
                   'Place 100 wards', 'Place 200 wards', 'Place 300 wards',
                   'Place 500 wards', 'Kill 50 wards', 'Kill 100 wards', 'Kill 200 wards',
                   'Win 6 games in a row', 'Win 8 games in a row', 'Win 10 games in a row',
                   'Lose 5 games in a row', 'Win a game in under 20:30',
                   'Win a game without byuing a recommended item', 'Win a classic 5v5',
                   'Win a classic 3v3', 'Win an ARAM', 'Win a special mode', 'Win a game in each gamemode',
                   'Play the tutorial', 'Win a game with at least 4 items with an active',
                   'Spend 1.000.000 gold', 'Get a killingspree of 4', 'Get a killingspree of 8',
                   'Get a killingspree of 12', 'Play a game without flash', 'Have a game with a duration of over 60 min',
                   'Play 3 stealth champs', 'Play 3 different stealth champs', 'Play 3 void champs',
                   'Play 3 different void champs', 'Win 1 game with Teemo', 'Win 2 games with Teemo',
                   'Win 3 games with Teemo', 'Play Teemo 2 times', 'Play Teemo 3 times', 'Play Teemo 4 times',
                   'Unlock the base level of all achievements', 'Win a game with all of the free-to-play champs']
    points = ['5', '5', '5', '10', '20', '40', '10', '20', '40', '10', '20', '40', '10', '20', '40', '10', '20', '40',
              '-40', '10', '20', '40', '10', '20', '40', '10', '10', '10', '5', '5', '5', '5', '10', '5', '5', '20',
              '10', '20', '40', '5', '5', '5' , '5', '5', '5', '10', '10', '0', '-5', '-5', '-5', '20', '20']
    name = ['Yordle Lover', 'Yordle Power', 'First Win!', 'Get the hang of it', 'Enemy slayer!', 'Bath in their blood!',
            'One-Trick Pony', 'Look at that champion pool!', 'Gotta master them all!', 'Allowance money', 'Bling Bling',
            'PVE master', 'I am helping out!', 'AoE damage FTW!', 'Gangplank master', 'Life savior', 'Support main',
            'Nothing can hide from your sight', 'Not see the forest for the trees', 'Ward seeker', 'Vision denied',
            'Living in the darkness', 'Lucky run', 'Climbing the ladder', 'Strike!', 'You can not always win',
            'Surrender at 20', 'Rebel', 'Classic', 'Vilemaw > Nashor', 'No time to farm', 'Play for fun',
            'Master all the modes', 'Back to the roots', 'Because 4 abilities are not enough', 'Millionaire',
            'Four in a row', 'Champions are for farming', 'PVP Master', 'No need to flash', '1h game', 'Can not see me',
            'Catch me if you can', 'Oh darn!', 'Dweller of the void', 'Teemo on duty!', 'Stop it!', 'Told you!',
            'Nobody likes Teemo', 'I mean it', 'Are you happy now?', 'Unlock Pro', 'Free elo']
    conn_string = "host='" + HOST + "' dbname='" + DBNAME + "' user='" + USER + "' password='" + PASS + "'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = "INSERT INTO achievement(name, description, points) VALUES (%s,%s,%s);"
    for i, desc in enumerate(description):
        data = (name[i], desc, points[i])
        cursor.execute(query, data)
        conn.commit()
