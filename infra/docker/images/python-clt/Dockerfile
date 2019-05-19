FROM python:3.7.3

LABEL maintainer = "Guilherme Muller <guilherme.muller.m@gmail.com>"
LABEL version = 0.0.1
LABEL description = "This image is used to run the command line tools of the application"

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install click flask requests