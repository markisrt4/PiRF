#!/bin/bash
set -e

URL="http://127.0.0.1/tar1090"

if command -v curl >/dev/null 2>&1; then
    curl --silent --fail --max-time 3 "$URL" >/dev/null
fi
