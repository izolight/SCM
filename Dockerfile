FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt -U
RUN chmod u+x entrypoint.sh
EXPOSE 8000
CMD ["/bin/bash", "entrypoint.sh"]
