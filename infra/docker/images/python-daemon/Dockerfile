FROM python:3.7.3

LABEL maintainer = "Guilherme Muller <guilherme.muller.m@gmail.com>"
LABEL version = 0.0.3
LABEL description = "This image is used to run the daemon service written in python"

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install --upgrade pip
RUN pip install pymongo
RUN pip install redis
RUN pip install pandas