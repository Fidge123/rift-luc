# League Unlock Challenge #

League Unlock Challenge uses data about your League of Legend games provided by the Riot Developer API to give you points for several kinds of achievements. You can form a league with friends for a fun competition to be the best at the League Unlock Challenge!

## Dependencies ##

1. Postgres
2. Postgrest
3. Python > 3
4. Virtualenv
5. Node.JS
6. Bower

<TODO>

## Setup ##
<TODO>

### Database scripts ###

There are scripts available that will create the necessary postgres tables and populate it with data. To use them it is recommened to setup a virtualenv for it first.

Bash:
``` bash
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r db_scripts/requirements.txt
```

Fish:
``` bash
virtualenv --no-site-packages --distribute .env; and source .env/bin/activate.fish; and pip install -r db_scripts/requirements.txt
```

This command creates a virtualenv, activates it and installs required libraries.

``` bash
deactivate
```

This command will deactivate the virtualenv.

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
