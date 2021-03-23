FROM python:3.9.0-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y
RUN apt install -y libpq-dev gcc
# RUN apt install -y gettext

RUN pip install --upgrade pip
#RUN pip install --upgrade pipenv

# Set work directory in container
WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system

# Copy Project source code
COPY . /app/