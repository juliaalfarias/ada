FROM python:3.7

ENV OPEN_JDK_VERSION 8
ENV JAVA_HOME  /usr/lib/jvm/java-${OPEN_JDK_VERSION}-openjdk-amd64

RUN echo "deb http://ftp.us.debian.org/debian stretch main" >> /etc/apt/sources.list && \
    apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | tee /etc/apt/sources.list.d/stretch-backports.list

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${OPEN_JDK_VERSION}-jre-headless" \
    ca-certificates-java && \
    update-ca-certificates -f && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir app

COPY app.py app/app.py
COPY models/ app/models/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 7000

WORKDIR /app

ENTRYPOINT [ "python3", "/app/app.py" ]