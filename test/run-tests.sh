#!/bin/bash

set -e

python3 -m pip install -r requirements.txt

python3 -m pip install pytest
python3 -m pip install pytest-cov
python3 -m pip install cryptography
pytest