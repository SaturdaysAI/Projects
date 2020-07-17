FROM python:3.8-slim

# RUN apt-get update
# RUN apt -y upgrade
# RUN apt-get -y install --no-install-recommends

# creating new user
RUN useradd -m -U -u 1000 flask

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# creating wrking directory
RUN mkdir /mnt/code
WORKDIR /mnt/code

# install dependencies
RUN pip3 install --upgrade pip
COPY ./covid_app/requirements.txt /mnt/code/
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chown -R flask:flask /mnt/code
RUN find /mnt/code -type f -exec chmod 644 {} \;
RUN find /mnt/code -type d -exec chmod 755 {} \;

VOLUME ["/mnt/code"]

USER flask

