FROM python:3.9-slim

WORKDIR /app


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/simple-cron


RUN chmod 0644 /etc/cron.d/simple-cron


CMD ["cron", "-f"]
