#!/usr/bin/env python3
"""Take argument"""

from sys import argv
import GetRecentMatches
import RegisterPlayer

if len(argv) == 1:
    print("Please give an argument")
elif argv[1] == "update":
    GetRecentMatches.get_all_recent_matches()
elif argv[1] == "register":
    if len(argv) != 7:
        print("Wrong number of argument: \n" +
              "Schema: main.py register 'name' 'region' 'email' 'password' 'leaguid'")
    else:
        RegisterPlayer.register_player(argv[2], argv[3], argv[4], argv[5], argv[6])
