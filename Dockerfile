FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && apt-get install -y -q build-essential python3-pip python3-dev
RUN pip3 install -U pip setuptools wheel && pip3 install gunicorn uvloop httptools

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY service/ /app

ENV ACCESS_LOG=${ACCESS_LOG:-/proc/1/fd/1}
ENV ERROR_LOG=${ERROR_LOG:-/proc/1/fd/2}

ENTRYPOINT /usr/local/bin/gunicorn \
    -b 0.0.0.0:80 \
    -w 4 \
    -k uvicorn.workers.UvicornWorker main:app \
    --chdir /app \
    --access-logfile ${ACCESS_LOG} \
    --error-logfile ${ERROR_LOG}
    