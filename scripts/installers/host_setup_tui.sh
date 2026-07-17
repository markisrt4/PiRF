#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$PROJECT_ROOT}"

if ! command -v whiptail >/dev/null 2>&1; then
  echo "[!] whiptail is not installed. Install it with: sudo apt install -y whiptail"
  exit 1
fi

if whiptail --title "OpenRoadCode Raspberry Pi installer" --yesno "Would you like to run the interactive installer?" 10 60; then
  :
else
  exit 0
fi

FEATURES=(
  "base|Core system dependencies"
  "core-ui|Browser/UI support"
  "gps|GPS daemon and Python support"
  "radio|RTL-SDR and radio support"
  "streamlit|Streamlit dashboard support"
  "adsb|ADS-B/readsb support"
  "bluetooth|Bluetooth support"
  "automotive|Automotive/OBD support"
  "spotify|Spotify integration extras"
  "sdrpp|SDR++ support"
)

OPTIONS=()
for entry in "${FEATURES[@]}"; do
  feature="${entry%%|*}"
  description="${entry#*|}"
  case "$feature" in
    base|gps|streamlit|bluetooth|automotive)
      OPTIONS+=("$feature" "$description" ON)
      ;;
    *)
      OPTIONS+=("$feature" "$description" OFF)
      ;;
  esac
done

SELECTED=$(whiptail --title "Choose feature bundles" --checklist \
  "Select the feature bundles to install:" 24 90 12 \
  "${OPTIONS[@]}" 3>&1 1>&2 2>&3)

status=$?
if [[ $status -ne 0 ]]; then
  exit 0
fi

ARGS=()
for feature in ${SELECTED}; do
  ARGS+=(--feature "$feature")
done

if [[ " $SELECTED " != *" base "* ]]; then
  ARGS+=(--feature base)
fi

if [[ -z "${SELECTED}" ]]; then
  ARGS+=(--feature base)
fi

if [[ " $SELECTED " == *" sdrpp "* ]]; then
  ARGS+=(--install-sdrpp)
fi

if [[ " $SELECTED " == *" radio "* ]]; then
  ARGS+=(--install-radio)
fi

bash "$PROJECT_DIR/scripts/installers/host_setup.sh" "${ARGS[@]}"
