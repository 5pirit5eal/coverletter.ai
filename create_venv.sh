#!/bin/bash
python -m venv .venv --prompt coverletter
source .venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt