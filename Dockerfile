FROM debian:latest

RUN DEBIAN_FRONTEND=noninteractive
ENV TZ=Africa/Algiers

RUN apt-get -qq -y install apt-transport-https
RUN apt-get update
RUN apt-get -qq -y install apt-utils cron
RUN apt-get -qq -y --fix-missing install python3-pip python3-pip python3-dev default-libmysqlclient-dev
RUN pip3 install uwsgi
RUN apt-get -qq -y install graphviz
ENV PYTHONPATH="/usr/bin/python3"


WORKDIR /data
COPY . .
RUN pip3 install -q -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
