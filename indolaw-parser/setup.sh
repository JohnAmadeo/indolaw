#!/usr/bin/env bash
if [[ $# != 3 ]]; then
  echo "./cleanup.sh [YEAR] [NUMBER] [NICKNAME]"
  exit
fi

YEAR=$1
NUMBER=$2
NICKNAME=$3

ORIGINAL_FILENAME="UU_NO_${NUMBER}_${YEAR}"
NEW_FILENAME="uu-${YEAR}-${NUMBER}-${NICKNAME}"
NEW_FILENAME_NO_NICKNAME="uu-${YEAR}-${NUMBER}"

mv ~/Downloads/${ORIGINAL_FILENAME}.PDF ./raw-laws/${NEW_FILENAME}.pdf
mv ~/Downloads/${ORIGINAL_FILENAME}.PDF.txt ./raw-laws/${NEW_FILENAME}.txt

cp ./raw-laws/${NEW_FILENAME}.txt ./${NEW_FILENAME_NO_NICKNAME}.txt
cp ./${NEW_FILENAME_NO_NICKNAME}.txt ./${NEW_FILENAME_NO_NICKNAME}-mod.txt

tput setaf 2;
echo "Moved files from ~/Downloads to /indolaw/indolaw-parser"
tput sgr0;