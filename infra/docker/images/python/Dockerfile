FROM python:3.7.3

LABEL maintainer = "Guilherme Muller <guilherme.muller.m@gmail.com>"
LABEL version = 0.0.1
LABEL description = "This image is used to run code writen in python that are, at this moment, the command line tools and the daemon service"

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install click flask requests