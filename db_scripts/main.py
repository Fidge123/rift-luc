#!/usr/bin/env python3
"""Take argument"""

import sys
import GetRecentMatches
import RegisterPlayer

if len(sys.argv) == 1:
    print("Please give an argument")
elif sys.argv[1] == "update":
    GetRecentMatches.get_all_recent_matches()
elif sys.argv[1] == "register":
    if len(sys.argv) != 7:
        print("Wrong number of argument: \n" +
              "Schema: main.py register 'name' 'region' 'email' 'password' 'leaguid'")
    else:
        RegisterPlayer.register_player(argv[2], argv[3], argv[4], argv[5], argv[6])
