FROM ubuntu:bionic

RUN \
 apt-get update \
 && apt-get install -y -q curl gnupg \
 && curl -sSL 'http://p80.pool.sks-keyservers.net/pks/lookup?op=get&search=0x8AA7AF1F1091A5FD' | apt-key add -  \
 && echo 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu/chime/stable bionic universe' >> /etc/apt/sources.list \
 && apt-get update --fix-missing

RUN apt-get install -y --allow-unauthenticated -q python3-grpcio-tools \
    python3-pip \
    python3-sawtooth-rest-api \
    python3-sawtooth-sdk


# Set work directory
WORKDIR /project/thutech
COPY . /project/thutech/

## Install dependencies
#RUN pip install pipenv
#COPY Pipfile Pipfile.lock /code/
#RUN pipenv install --system
#
## Copy project
#COPY . /code/

RUN pip3 install -r client/requirements.txt
