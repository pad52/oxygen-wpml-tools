#!/bin/bash

for f in ../texts/jsons/*.json; do
  ./oxy_translator.py -o $f $f".csv"
done

