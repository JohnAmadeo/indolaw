#!/usr/bin/env bash
rm -rf missing-laws.txt

declare -a allLaws
declare -a currentLaws

currentLawsDir=`ls ./raw-laws/*.txt`
for eachfile in $currentLawsDir
do
    currLawFile=$(echo `basename $eachfile` | cut -d '-' -f 1-3 | cut -d '.' -f1);
    currentLaws+=($currLawFile)
done

allLawsDir=`ls ./metadata/uu_html/*.html`
for eachfile in $allLawsDir
do
    currFile=$(echo `basename $eachfile` | cut -d '.' -f 1);
    if [[ ! " ${currentLaws[@]} " =~ " ${currFile} " ]]; then
        echo $currFile >> missing-laws.txt
    fi
done



