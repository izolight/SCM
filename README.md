# Simple Club Manager

Simple Club Manager (SCM) is an application for sports clubs to manage their members.
This application is for the "Project 1" class at BFH.

bla

## dev environment

### Requirements:

- python 3.6+
- pycharm
- docker

### setup

```bash
git clone https://gitlab.com/ch.bfh.ti.keusa1/SimpleClubManager-SCM
python3 -m venv SimpleClubManager-SCM
cd SimpleClubManager-SCM
. bin/activate # windows -> \Scripts\activate.bat
pip install django mysqlclient docker-compose
```

### start db

```bash
# in SimpleClubManager-SCM directory
docker-compose up -d
```