#!/usr/bin/env bash 

envsubst < /etc/nginx/conf.d/nginx.template > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
