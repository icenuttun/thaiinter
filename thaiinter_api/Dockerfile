# pull official base image
FROM python:3.10.6-alpine

# set work directory
WORKDIR /usr/src/thaiinter_api
RUN mkdir static
RUN mkdir media

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache postgresql-client \
    && apk add --no-cache freetype-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/thaiinter_api/entrypoint.sh
RUN chmod +x /usr/src/thaiinter_api/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/thaiinter_api/entrypoint.sh"]