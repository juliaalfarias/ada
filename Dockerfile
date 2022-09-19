FROM python:3.7

RUN echo "deb http://ftp.us.debian.org/debian stretch main" >> /etc/apt/sources.list && \
    apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'deb http://ftp.debian.org/debian stretch-backports main' | tee /etc/apt/sources.list.d/stretch-backports.list

# RUN pip install setuptools==39.1.0

RUN python3 -m pip install --upgrade pip
#RUN pip install --upgrade setuptools==41.2.0
RUN pip3 install --upgrade --force-reinstall --no-cache-dir setuptools_rust
RUN pip3 install --upgrade --force-reinstall --no-cache-dir cryptography

RUN mkdir app

COPY app.py app/app.py
COPY models/ app/models/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 7000

WORKDIR /app

ENTRYPOINT [ "python3", "/app/app.py" ]