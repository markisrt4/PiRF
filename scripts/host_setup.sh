#!/bin/bash

sudo apt update
sudo apt install git curl lighttpd

python3 -m venv venv
source venv/bin/activate
pip install streamlit requests geocoder streamlit-autorefresh gpsd-py3
