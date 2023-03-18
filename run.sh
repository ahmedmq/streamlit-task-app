#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
cd "$SCRIPT_DIR" || exit

python"$1" -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt --require-virtualenv

streamlit run src/Home.py
