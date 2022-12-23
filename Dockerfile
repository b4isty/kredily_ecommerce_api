# Pull base image
FROM python:3.9

# install tzdata
# RUN apt-get update &&
RUN apt-get install -y tzdata
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /code/
