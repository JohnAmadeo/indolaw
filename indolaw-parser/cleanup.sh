#!/usr/bin/env bash
if [[ $# != 2 ]]; then
  echo "./cleanup.sh [YEAR] [NUMBER]"
  exit
fi

GREEN='\033[0;32m'

YEAR=$1
NUMBER=$2

FILENAME="uu-${YEAR}-${NUMBER}"

tput setaf 2;
cp ${FILENAME}-mod.json ../indolaw-nextjs/laws/${FILENAME}.json
echo "(1) Moved ${FILENAME}-mod.json to /indolaw-nextjs/laws/${FILENAME}.json"

mv ${FILENAME}* ./laws/
echo "(2) Moved all files starting w/ ${FILENAME} to /laws folder"

tput sgr0;