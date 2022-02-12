#!/bin/bash
# shellcheck source=/dev/null
/usr/bin/python3 -m venv --copies "$1"
source "$1"/bin/activate
#pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install --upgrade pip
pip install -r "$2"
deactivate
