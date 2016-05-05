# League Unlock Challenge #

League Unlock Challenge uses data about your League of Legend games provided by the Riot Developer API to give you points for several kinds of achievements. You can form a league with friends for a fun competition to be the best at the League Unlock Challenge!

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

### Start database server ###

Read how to start the database server: http://www.postgresql.org/docs/current/static/server-start.html

### Database scripts ###

<TODO>

### Python scripts ###

<TODO>

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
