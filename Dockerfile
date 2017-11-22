FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmysqlclient-dev \
	    netcat-openbsd \
	    gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt -U
EXPOSE 8000
WORKDIR /usr/src/app
COPY util/entrypoint.sh ./
CMD ["/bin/bash", "entrypoint.sh"]
