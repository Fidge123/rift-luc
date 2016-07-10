#!/usr/bin/env python3
"""Take argument"""

from sys import argv
import getopt
import GetRecentMatches
import RegisterPlayer

def usage():
    """Show usage help"""
    print("Schema: main.py --update \n" +
          "main.py --register --name='name' --region='region' " +
          "--emai='email' --password='password' --leagueid='leagueid' \n" +
          "main.py --register -n 'name' -r 'region -e 'email' -p 'password' " +
          "-l 'leagueid'")

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
                              "email=", "password=", "leagueid="])

        for opt in opts[0]:
            if opt[0] in ("-h", "--help"):
                usage()
            elif opt[0] == "--update":
                GetRecentMatches.get_all_recent_matches()
            elif opt[0] == "--register":
                register(opts)

    except getopt.GetoptError as err:
        print(err)
        usage()

if __name__ == '__main__':
    main()
