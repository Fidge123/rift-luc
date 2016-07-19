# League Unlock Challenge #

League Unlock Challenge uses data about your League of Legend games provided by the Riot Developer API to give you points for several kinds of achievements. You can form a league with friends for a fun competition to be the best at the League Unlock Challenge!

The project is currently ongoing and not yet fully functional.

## Dependencies ##

1. PostgreSQL
2. PostgREST
3. Python 3
4. Virtualenv
5. Node.JS
6. Bower

If you are using MacOSX you should install homebrew by opening the terminal and running

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Install PostgreSQL ###

PostgreSQL is a open source database that is used in this project to store the data we receive from the API. You can get more information on http://www.postgresql.org/

**Ubuntu:**

``` bash
sudo apt-get install postgresql postgresql-contrib
```

**MacOSX with homebrew:**

``` bash
brew install postgres
```

**Windows:**

Download and install binary from http://www.postgresql.org/download/

### Get PostgREST ###

> PostgREST serves a fully RESTful API from any existing PostgreSQL database. It provides a cleaner, more standards-compliant, faster API than you are likely to write from scratch.

You can get more information on http://postgrest.com/

To use PostgREST you can download the release for you platform from https://github.com/begriffs/postgrest/releases/tag/v0.3.1.1 and extract it with
``` bash
tar zxf postgrest-[version]-[platform].tar.xz
```

### Install Python ###

**Linux:**

Linux distribution usually come with python 3 preinstalled. If both python 2 and 3 are installed, you might need to run it as `python3`. You can make sure you have the right version with `python -v`.

**MacOSX with homebrew:**

Install it with

```
brew install python
```

**Windows:**

Download the official release here and execute to install: https://www.python.org/downloads/release/python-351/

This will come with pip automatically. If your installation does not have it read here https://pip.pypa.io/en/latest/installing/

### Install virtualenv & python dependencies ###

To install virtualenv, run `pip install virtualenv`.

Create virtualenv and install the dependencies for the python scripts:

Bash:
``` bash
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r db_scripts/requirements.txt
```

Fish:
``` bash
virtualenv --no-site-packages --distribute .env; and source .env/bin/activate.fish; and pip install -r db_scripts/requirements.txt
```

To deactivate the virtualenv again:

``` bash
deactivate
```

### Install Node.JS ###

**Linux:**

``` bash
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**MacOsX with homebrew:**

``` bash
brew install node
```

**Windows:**

Download and install the binary: https://nodejs.org/en/download/

**After installing:**

Once Node.JS and NPM are installed you can run
```
npm install
```
to install the required javascript packages.

### Install Bower ###

``` bash
npm install -g bower
bower install
```

## Setup ##

### Start PostgreSQL server ###

Read how to start the database server: http://www.postgresql.org/docs/current/static/server-start.html

Once the server is started, create a database

``` bash
createdb luc
```

### Start PostgREST server ###

Start PostgREST server on default port 3000
```
postgrest postgres://localhost:5432/luc -a postgres -j <secret>
```
For more information read http://postgrest.com/install/server/

You can now use the PostgREST API to register, login and read the available data.

To create a new user, you can use the signup function.

`POST localhost:3000/rpc/signup`

Body:

``` json
{
    "leaguename": "Fidge1234",
    "region": "EUW",
    "pass": "ENTER-YOUR-PASSWORD-HERE"
}
```

Use the login function to receive a jwt token to authenticate with.

`POST localhost:3000/rpc/login`

Body:

``` json
{
    "leaguename": "Fidge1234",
    "region": "EUW",
    "pass": "ENTER-YOUR-PASSWORD-HERE"
}
```

Response:

``` json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZvb0BiYXIuY29tIiwicm9sZSI6ImF1dGhvciJ9.KHwYdK9dAMAg-MGCQXuDiFuvbmW-y8FjfYIcMrETnto"
}
```

You can get account information with the current_id function, if you provide the jwt token.

`POST localhost:3000/rpc/current_id`

Header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZvb0BiYXIuY29tIiwicm9sZSI6ImF1dGhvciJ9.KHwYdK9dAMAg-MGCQXuDiFuvbmW-y8FjfYIcMrETnto
```

Response:

``` json
[{
    "id": "12345678",
    "region": "euw"
}]
```

To make requests against the database, you also have to provide your token.

`GET localhost:3000/player?id=eq.12345678`

Header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZvb0BiYXIuY29tIiwicm9sZSI6ImF1dGhvciJ9.KHwYdK9dAMAg-MGCQXuDiFuvbmW-y8FjfYIcMrETnto
```

Response:

``` json
[
  {
    "id": 12345678,
    "leaguename": "fidge1234",
    "region": "euw",
    "iconid": 1,
    "leagueid": null,
    "wins": 0,
    ...
    "points": 0
  }
]
```

### Python scripts ###

Too use the python scripts, you will need to create key-file with your Riot API Key first.

``` bash
echo ENTER-YOUR-KEY-HERE > KEY
```

To use the python scripts that are updating/filling your database, you will need to create a db_config file with your hostadress of your postgresql server, the name of your db, the user_name for your database and your password for this user.
All this information should each be stored per line.

``` bash
echo HOSTADRESS >> DB_CONFIG
echo DB_NAME >> DB_CONFIG
echo USER_NAME >> DB_CONFIG
echo PASSWORD >> DB_CONFIG
```

Once this information is provided, you can run the main.py to trigger all necessary functionality.

``` bash
./main.py -h # help
./main.py --reset # reset or create the database and fill it with static data from the API
./main.py --register -n 'name' -r 'region' -p 'password' # convenience function to register a user
./main.py --verify # trigger a verification process which creates an entry in the player table for all registered users
./main.py --update # load recent games for all players and write calculated points to db
```

## Deployment ##

#### Local Deployment for Development

You can use the serve gulp task to deploy locally.

```sh
gulp serve
```

This outputs an IP address you can use to locally test and another that can be used on devices connected to your network.

### Github Pages ###

1. In app.js change `app.baseUrl = '/';` to `app.baseUrl = '/league-unlock-challenge/';`
2. Run `gulp build-deploy-gh-pages` from command line
3. To see changes wait 1-2 minutes then load Github pages for your app (ex: https://fidge123.github.io/league-unlock-challenge/)
