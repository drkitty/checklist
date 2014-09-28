#!/usr/bin/env bash

set -o errexit
shopt -s nullglob

if ! [[ -d .env ]]; then
    virtualenv .env -p $(which python3)
fi

source .env/bin/activate

for f in requirements/*; do
    pip3 install -r "$f"
done
