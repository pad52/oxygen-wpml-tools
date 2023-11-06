#!/usr/bin/env python3

##
# This short script helps translating Wordpress shop & Extra product options csv_files 
#
# 
#
#   This code is in the Public Domain (or CC0 licensed, at your option.)
#   Unless required by applicable law or agreed to in writing, this
#   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.
##

import os, sys, csv, polib, re 
import pandas as pd
from thefuzz import fuzz

DEBUG = 1
ENABLE_FUZZY = 1 #Disabled for urls
FUZZY_RATIO = 98



MODE_OUTPUT = 0
MODE_INPUT = 1
MODE_OUTPUT_POT = 2
MODE_INPUT_JSON = 3
MODE_INPUT_POT = 4

search_keys_epo = ["header_title", "header_subtitle", "radiobuttons_header_title", "radiobuttons_header_subtitle", "multiple_radiobuttons_options_title", "multiple_radiobuttons_options_value","upload_header_title","product_header_title","product_header_subtitle","product_placeholder"]
search_keys_shop = ["Name","Short description","Meta: short_excerpt","Meta: pb_product_prop1_text","Meta: pb_product_prop1_title","Meta: pb_product_prop2_text","Meta: pb_product_prop2_title","Meta: pb_product_prop3_title","Meta: pb_product_prop3_text"]

search_keys = search_keys_epo + search_keys_shop

exclude = ["<style", "<table"]


def find_content(csv_obj, results_list):
    for col in search_keys:
        if col in csv_obj:
            if DEBUG:
                print(f"{col} found")
            values = data[col].tolist()
            
            for value in values:
                if (len( value.strip() ) != 0):
                    if not any([x in value for x in exclude]):
                        results_list.append(value)
                    else:
                        if DEBUG:
                            print(f"EXCLUDING {value}")

def update_po_content(csv_obj, msgid, msgstr, index=0):
    for col in search_keys:
        if col in csv_obj:
            if DEBUG:
                print(f"{col} found")
            values = data[col].tolist()
            
            for value in values:
                
                if( ENABLE_FUZZY and 
                    not (value.startswith("https:") or value.startswith("http:")) ):
                    ratio = fuzz.ratio(value, msgid)

                    if ratio > FUZZY_RATIO:
                        if(DEBUG):
                            print(f"MATCHED - {value} - AGAINST - {msgid} - AT {ratio}%")
                        csv_obj.replace( to_replace=value, value=msgstr, inplace=True )
                        index += 1
                else:
                    #val_after = json_obj[key].replace(msgid,msgstr)
                    if(value.strip() == msgid.strip()):
                        if(DEBUG):
                            print(f"REPLACED - {value} WITH {msgstr}")
                        csv_obj.replace( to_replace=value, value=msgstr, inplace=True )
                        index += 1
                
    return index


# MAIN

if len(sys.argv) < 2:
    print("Usage\n \
        From CSV to POT: csv_translator.py -p [CSV INPUT FILE] (optional)[POT OUTPUT FILE] or\n \
        From PO to CSV: csv_translator.py -c [CSV (ORIGINAL LANGUAGE) INPUT FILE] [PO INPUT FILE] (optional)[CSV OUTPUT FILE] or\n \
        If the optional [OUTPUT FILE] it is not specified the output will be stdout.")
    sys.exit()
elif len(sys.argv) < 3:
    print("ERROR: Give me a json file at least!")
    sys.exit()
elif len(sys.argv) >= 3:
    
    request = str(sys.argv[1])
    
    if(str(sys.argv[1]) == "-p"):
        mode = MODE_OUTPUT_POT
    
        if len(sys.argv) == 4:
            pot_filename = str(sys.argv[3])
            
            pot_file = open(pot_filename,'a');
        elif len(sys.argv) > 4:
            print("ERROR: Too many arguments!")
            sys.exit()
    elif(str(sys.argv[1]) == "-c"):
        mode = MODE_INPUT_POT
        print("MODE INPUT POT")
        if( len(sys.argv) == 4 or len(sys.argv) == 5):
            
            pot_filename = str(sys.argv[3])
            
            pot_file = open(pot_filename,'r')
            if len(sys.argv) == 5:
                csv_out_filename = str(sys.argv[4])
                
        elif len(sys.argv) > 5:
            print("ERROR: Too many arguments!")
            sys.exit()
    else:
        print("ERROR: Arguments -i, -o, -p, -j accepted only.")
        sys.exit()
        
else:
    print("ERROR: Too many arguments!")
    sys.exit()

 
# Opening CSV file
csv_in_filename = str(sys.argv[2])

# making data frame from csv
data = pd.read_csv( csv_in_filename, lineterminator="\n", quoting=csv.QUOTE_ALL, dtype="string")
data.fillna(value='', inplace=True)
data = data.replace(r'\n',' ', regex=True) 

if(mode == MODE_OUTPUT_POT):
    
    # Initialize an empty list to store the results
    results = []

    # Call the function to find and store "ct_content" values in the results list
    find_content(data, results)

    # Print the values of "ct_content" keys
    for idx, value in enumerate(results, start=1):
        value = value.replace( '\\' , '\\\\' )
        value = value.replace( '"',r'\"' )
        
        if len(sys.argv) > 3:
            pot_file.write( '#: {0}:{1} \n'.format( os.path.basename(csv_in_filename) ,idx) )
            pot_file.write('msgid "{0}"     \n'.format( value ) )
            pot_file.write('msgstr ""     \n\n')

        else:
            print(f"Value {idx}: {value}")
            
    if len(sys.argv) > 3:
        pot_file.close()

        
elif(mode == MODE_INPUT_POT):
    
    # Initialize an empty list to store the results
    results = []

    # Call the function to find and store "ct_content" values in the results list
    find_content(data, results)
    
    
    po_data = polib.pofile( pot_filename )
    
    idx = 0

    for entry in po_data:
        idx += update_po_content(data, entry.msgid, entry.msgstr)

    print(f"{idx} occurences updated out of {len(results)} found.")
            
    if len(sys.argv) == 5:
        data.to_csv(csv_out_filename)

    else:
        print(data)
    

sys.exit()
    
