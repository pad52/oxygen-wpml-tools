#!/bin/bash

#
# This script makes the jsons out of the original json and the PO file.
#

DEST_LANG="en"
SOURCE_LANG="it"

SOURCE="../texts/jsons/$SOURCE_LANG/*.json"
PO_FILE="../texts/pots/oxygen-pages_English.po"

for f in $SOURCE; do
  echo "Doing ./oxy_translator.py -j $f $PO_FILE $DEST_FILE"
  DEST_FILE=${f//"$SOURCE_LANG"/"$DEST_LANG"}
  ./oxy_translator.py -j $f $PO_FILE $DEST_FILE
  
  cat $DEST_FILE | xclip -sel clip
  echo "paste $DEST_FILE and press any key to continue..."
  read -s -n 1
done

