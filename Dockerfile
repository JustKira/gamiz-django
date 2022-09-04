FROM python:3.9.13-buster

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN apt-get update && \
    apt-get -y upgrade  && \
    apt-get -y install git bash
RUN apt-get -y install libglu1
RUN pip install -r requirements.txt
COPY ./backend-dock /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

