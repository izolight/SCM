#! /bin/bash

cd /project/SimpleClubManager-SCM
git pull
. ../venv/bin/activate
docker-compose -f docker-compose-server.yml up -d
deactivate
