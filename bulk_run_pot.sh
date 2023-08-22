#!/bin/bash

for f in ../texts/jsons/it/*.json; do
  ./oxy_translator.py -p $f "../texts/pots/it-all.pot"
done

