#!/bin/bash

#
# This script makes a single pot file out of many csvs.
# Since it append every occurence, be sure that the destination file is empty
#

LANG="it"
SOURCE="../../texts/csvs/$LANG/*.csv"
DEST="../../texts/pots/$LANG-csv-everything.pot"

for f in $SOURCE; do
  ./csv_translator.py -p $f $DEST
  echo "$f done"
done

