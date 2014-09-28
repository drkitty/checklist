#!/usr/bin/env bash

source settings/server.sh

uwsgi_cmd="uwsgi -H .env -s $SOCKET_FILE -w runserver:app $*"
sudo -u $NGINX_USER bash -c "source .env/bin/activate && $uwsgi_cmd"
