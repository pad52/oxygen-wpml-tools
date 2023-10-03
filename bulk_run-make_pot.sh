#!/bin/bash

#
# This script makes a single pot file out of many jsons.
# Since it append every occurence, be sure that the destination file is empty
#

LANG="it"
SOURCE="../texts/jsons/$LANG/*.json"
DEST="../texts/pots/$LANG-all.pot"

for f in $SOURCE; do
  ./oxy_translator.py -p $f $DEST
done

