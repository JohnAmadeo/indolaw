#!/usr/bin/env bash
if [[ $# != 2 ]]; then
  echo "./cleanup.sh [YEAR] [NUMBER]"
  exit
fi

YEAR=$1
NUMBER=$2

open https://www.google.com/search?q=uu+${NUMBER}+${YEAR}+hukumonline