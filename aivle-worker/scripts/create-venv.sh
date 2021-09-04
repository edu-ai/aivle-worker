#!/bin/bash
# shellcheck source=/dev/null
python3 -m venv --copies "$1"
source "$1"/bin/activate
pip install -r "$2"
deactivate
