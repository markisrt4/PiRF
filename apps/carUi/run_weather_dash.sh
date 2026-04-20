#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

exec streamlit run weather_dash.py \
  --server.address 0.0.0.0 \
  --server.port 8501