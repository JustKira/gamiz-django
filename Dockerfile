FROM python:3.9.13-buster

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN apt-get update && \
    apt-get -y upgrade  && \
    apt-get -y install git bash
RUN apt-get -y install libglu1
RUN apt-get -y install python-certbot-nginx
RUN pip install -r requirements.txt

RUN -it --rm -p 80:80 --name certbot \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    certbot/certbot certonly --standalone --staging -d 165.227.143.235
COPY ./backend-dock /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

