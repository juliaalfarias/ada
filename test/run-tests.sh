#!/bin/bash

set -e

python3 -m pip install -r requirements.txt

python3 -m pip install pytest
python3 -m pip install pytest-cov
python3 -m pip install cryptography==38.0.1
python3 -m pip install setuptools==65.3.0
python3 -m pip install setuptools-rust==1.1.2

pytest