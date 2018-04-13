#!/bin/bash

# Extracts sites from DWD website html where bee flight activity forecasts are available.

# prerequisites:
# apt-get install recode

DWD_BASE_PATH="DE/fachnutzer/freizeitgaertner/1_gartenwetter"
DWD_BASE_URL="https://www.dwd.de"

wget -qN -O _node.html $DWD_BASE_URL/$DWD_BASE_PATH/_node.html

FED_STATES=$(grep $DWD_BASE_PATH/ _node.html |grep title |cut -d\" -f4 |cut -d/ -f5)

for FED_STATE in $FED_STATES;do
  FED_STATE_UTF=$(grep /$FED_STATE _node.html |cut -d\" -f6 | recode html..utf8 )
  echo $FED_STATE, $FED_STATE_UTF
  wget -q -O $FED_STATE.html $DWD_BASE_URL/$DWD_BASE_PATH/$FED_STATE/_node.html
  SITES=$(grep $DWD_BASE_PATH/$FED_STATE/ $FED_STATE.html |grep class |grep -v steckbrief|cut -d\" -f4 |cut -d/ -f6)
  for SITE in $SITES;do
    SITE_UTF=$(grep /$SITE/_node.html $FED_STATE.html |grep -v related_0 |cut -d\" -f6 | recode html..utf8 )
    echo "  $SITE, $SITE_UTF"
  done
  rm $FED_STATE.html*
done > apicast_sites.txt

rm _node.html*

