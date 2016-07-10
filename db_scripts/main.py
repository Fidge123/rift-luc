#!/usr/bin/env python3
"""Take argument"""

from sys import argv
import getopt
import GetRecentMatches
import RegisterPlayer

def usage():
    print("Schema: main.py --update \n" +
          "main.py --register --name='name' --region='region' " +
          "--emai='email' --password='password' --leagueid='leagueid' \n" +
          "main.py --register -n 'name' -r 'region -e 'email' -p 'password' " +
          "-l 'leagueid'")
    
if len(argv) == 1:
    print("Please give an argument or use main.py -h/--help for options")
try:
    opts,args = getopt.getopt(argv[1:],"hn:r:e:p:l:",
                              ["help", "update","register","name=","region=",
                               "email","password=","leagueid="])
except getopt.GetoptError as err:
    print(err)
    usage()
register = False
for o, a in opts:
    if o in ("-h","--help"):
        usage()
    elif o == "--update":
        GetRecentMatches.get_all_recent_matches()
    elif o == "--register":
        register = True
if register:
    name, region, email, password, leagueid = ''
    for o,a in opts:
        if o in ("-n","--name"):
            name = a
        elif o in ("-r","--region"):
            region = a
        elif o in ("-e","--email"):
            email = a
        elif o in ("-p","--password"):
            password = a
        elif o in ("-l","--leagueid"):
            leagueid = a
    if name and region and password and leagueid and email:
        RegisterPlayer.register_player(name,region,email,password,leagueid)
    else:
        usage()
    
