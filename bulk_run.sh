#!/bin/bash

for f in ./jsons/*.json; do
  ./oxy_translator.py -o $f $f".csv"
done

