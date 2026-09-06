#!/usr/bin/env bash
set -o errexit

export PLAYWRIGHT_BROWSERS_PATH=0
python -m pip install --upgrade pip
pip install -r automation/requirements.txt
playwright install chromium


