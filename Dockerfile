FROM python:3.7

RUN echo "deb http://ftp.us.debian.org/debian stretch main" >> /etc/apt/sources.list && \
    apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | tee /etc/apt/sources.list.d/stretch-backports.list

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U pip setuptools

RUN mkdir app

COPY app.py app/app.py
COPY models/ app/models/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 7000

WORKDIR /app

ENTRYPOINT [ "python3", "/app/app.py" ]