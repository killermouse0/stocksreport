#! /bin/bash

source .venv/bin/activate

source secrets/tokens.sh
source secrets/aws.sh

python main.py
