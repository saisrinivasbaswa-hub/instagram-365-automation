#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r automation/requirements.txt
pip install playwright instagrapi Pillow
playwright install chromium
