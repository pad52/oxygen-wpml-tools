#!/bin/bash

for f in ../texts/jsons/*.json; do
  ./oxy_translator.py -p $f "export.pot"
done

