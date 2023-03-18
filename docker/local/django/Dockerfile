FROM python:3.10.0-slim-buster

ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

LABEL maintainer="maqboolthoufeeq.t@gmail.com"
LABEL owner="MaqboolThoufeeqT"
LABEL description="Development image for RealEstate Project"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
&& apt-get install -y build_essential \
&& apt-get install -y gettext \
&& apt-get install -y netcat gcc postgresql \
&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start  /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


ENTRYPOINT [ "/entrypoint" ]