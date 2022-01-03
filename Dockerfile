FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt 
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
COPY ./ /code/