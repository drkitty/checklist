#!/usr/bin/env bash

source settings/server.sh
sudo -u $NGINX_USER uwsgi -H .env -s $SOCKET_FILE -w runserver:app $*
