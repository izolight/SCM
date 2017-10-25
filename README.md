# Simple Club Manager

Simple Club Manager (SCM) is an application for sports clubs to manage their members.
This application is for the "Project 1" class at BFH.

bla

## Dev environment

### Requirements:

- python 3.6+
- pycharm
- docker

### setup

```bash
git clone https://gitlab.com/ch.bfh.ti.keusa1/SimpleClubManager-SCM
git checkout develop
python3 -m venv SimpleClubManager-SCM
cd SimpleClubManager-SCM
. bin/activate # windows -> \Scripts\activate.bat
pip install -r requirements.txt --upgrade
```

### start db

```bash
# in SimpleClubManager-SCM directory
docker-compose up -d
```

### setup django db

```bash
python manage.py makemigrations
python manage.py migrate
```
