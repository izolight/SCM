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

#### clone repository
##### ssh 
```bash
git clone git@gitlab.com:ch.bfh.ti.keusa1/SimpleClubManager-SCM.git
```
##### http
```bash
git clone https://gitlab.com/ch.bfh.ti.keusa1/SimpleClubManager-SCM
```
#### create python virtual env 
```bash
python3 -m venv SimpleClubManager-SCM
```
##### cd to dir and activate venv 
###### Linux/macOS
```bash
cd SimpleClubManager-SCM
. bin/activate
```
###### Windows
```bash
cd SimpleClubManager-SCM
Scripts\activate.bat
```

##### install requirements 
```bash
pip install -r requirements.txt --upgrade
```

### start db
in SimpleClubManager-SCM directory:
```bash
docker-compose up -d
```

### setup django db

```bash
python manage.py migrate
```

### apply db modifications

```bash
python manage.py makemigrations
python manage.py migrate
```


### trash db and re-create it 
in SimpleClubManager-SCM directory:
```bash
docker rm -f simpleclubmanagerscm_scm-db-server_1 
docker volume rm simpleclubmanagerscm_scm-db
docker-compose up -d
```

