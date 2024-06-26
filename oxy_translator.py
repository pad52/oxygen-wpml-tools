#!/usr/bin/env python3

##
# This short script helps translating Wordpress pages built with "Oxygen page builder" and translated with "WPML"
# 
# Step 1: copy the JSON in the Oxygen tab located in the "Edit page" Wordpress view and save it to a [JSON INPUT FILE]
# Step 3: run the script: "oxy_translator.py -o [JSON INPUT FILE] [CSV OUTPUT FILE]"
# Step 4: translate the generated [CSV OUTPUT FILE] using a spreadsheet editor 
#         use the "translation" column and save it as [CSV INPUT FILE]
# Step 5: run the script: "oxy_translator.py -i [JSON INPUT FILE] [CSV INPUT FILE] [JSON OUTPUT FILE]"
# Step 6: copy/paste the generated [JSON OUTPUT FILE] in the translated page of Wordpress
# 
#
#   This code is in the Public Domain (or CC0 licensed, at your option.)
#   Unless required by applicable law or agreed to in writing, this
#   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.
##

import os, sys, json,csv, polib,re 
import pandas as pd
from thefuzz import fuzz

DEBUG = 0
ENABLE_FUZZY = 1 #Disabled for urls
FUZZY_RATIO = 98



MODE_OUTPUT = 0
MODE_INPUT = 1
MODE_OUTPUT_POT = 2
MODE_INPUT_JSON = 3
MODE_INPUT_POT = 4

search_keys = ["ct_content", "url", "icon_box_heading", "icon_box_text"]
exclude = ["<style", "<table", "<span", "[oxygen"]


def find_content(json_obj, results_list):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key in search_keys:
                if (len( value.strip() ) != 0):
                    if not any([x in value for x in exclude]):
                        results_list.append(value)
                    else:
                        if DEBUG:
                            print(f"EXCLUDING {value}")
            elif isinstance(value, (dict, list)):
                find_content(value, results_list)
    elif isinstance(json_obj, list):
        for item in json_obj:
            find_content(item, results_list)


def update_content(json_obj, values_list, index=0):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key in search_keys:
                if index < len(values_list):
                    json_obj[key] = values_list[index]
                    index += 1
            elif isinstance(value, (dict, list)):
                index = update_content(value, values_list, index)
    elif isinstance(json_obj, list):
        for item in json_obj:
            index = update_content(item, values_list, index)
    return index

def update_po_content(json_obj, msgid, msgstr, index=0):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key in search_keys:
                
                if( ENABLE_FUZZY and 
                   not (json_obj[key].startswith("https:") or json_obj[key].startswith("http:")) ):
                    ratio = fuzz.ratio(json_obj[key], msgid)
   
                    if ratio > FUZZY_RATIO:
                        if(DEBUG):
                            print(f"MATCHED - {json_obj[key]} - AGAINST - {msgid} - AT {ratio}%")
                        json_obj[key] = msgstr
                        index += 1
                else:
                    #val_after = json_obj[key].replace(msgid,msgstr)
                    if(json_obj[key].strip() == msgid.strip()):
                        if(DEBUG):
                            print(f"REPLACED - {json_obj[key]} WITH {msgstr}")
                        json_obj[key] = msgstr
                        index += 1
                
                  
            elif isinstance(value, (dict, list)):
                index = update_po_content(value, msgid, msgstr, index)
    elif isinstance(json_obj, list):
        for item in json_obj:
            index = update_po_content(item, msgid, msgstr, index)
    return index


# MAIN

if len(sys.argv) < 2:
    print("Usage\n \
        From JSON to CSV: oxy_translator.py -o [JSON INPUT FILE] (optional)[CSV OUTPUT FILE] or\n \
        From CSV to JSON: oxy_translator.py -i [JSON INPUT FILE] [CSV INPUT FILE] (optional)[JSON OUTPUT FILE]\n \
        From JSON to POT: oxy_translator.py -p [JSON INPUT FILE] (optional)[POT OUTPUT FILE] or\n \
        From PO to JSON: oxy_translator.py -j [JSON (ORIGINAL LANGUAGE) INPUT FILE] [PO INPUT FILE] (optional)[JSON OUTPUT FILE] or\n \
        If the optional [OUTPUT FILE] it is not specified the output will be stdout.")
    sys.exit()
elif len(sys.argv) < 3:
    print("ERROR: Give me a json file at least!")
    sys.exit()
elif len(sys.argv) >= 3:
    
    request = str(sys.argv[1])
    
    if(request == "-o"):
        mode = MODE_OUTPUT
    
        if len(sys.argv) == 4:
            csv_filename = str(sys.argv[3])
            
            csv_file = open(csv_filename,'w');
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow( ['index','original_language','translation'] )
        elif len(sys.argv) > 4:
            print("ERROR: Too many arguments!")
            sys.exit()
    
    elif(str(sys.argv[1]) == "-i"):
        mode = MODE_INPUT
        
        if( len(sys.argv) == 4 or len(sys.argv) == 5):
            
            csv_filename = str(sys.argv[3])
            
            csv_file = open(csv_filename,'r')
            if len(sys.argv) == 5:
                json_out_filename = str(sys.argv[4])
                
                json_out_file = open(json_out_filename,'w')
        elif len(sys.argv) > 5:
            print("ERROR: Too many arguments!")
            sys.exit()
    elif(str(sys.argv[1]) == "-p"):
        mode = MODE_OUTPUT_POT
    
        if len(sys.argv) == 4:
            csv_filename = str(sys.argv[3])
            
            csv_file = open(csv_filename,'a');
        elif len(sys.argv) > 4:
            print("ERROR: Too many arguments!")
            sys.exit()
    elif(str(sys.argv[1]) == "-j"):
        mode = MODE_INPUT_POT

        if( len(sys.argv) == 4 or len(sys.argv) == 5):
            
            csv_filename = str(sys.argv[3])
            
            csv_file = open(csv_filename,'r')
            if len(sys.argv) == 5:
                json_out_filename = str(sys.argv[4])
                
                json_out_file = open(json_out_filename,'w')
        elif len(sys.argv) > 5:
            print("ERROR: Too many arguments!")
            sys.exit()
    else:
        print("ERROR: Arguments -i, -o, -p, -j accepted only.")
        sys.exit()
        
else:
    print("ERROR: Too many arguments!")
    sys.exit()

 
# Opening JSON file
json_filename = str(sys.argv[2])
json_file = open(json_filename, "r")

 
# returns JSON object as
# a dictionary
nested_json = json.load(json_file)

    

if(mode == MODE_OUTPUT):
    
    # Initialize an empty list to store the results
    results = []

    # Call the function to find and store "ct_content" values in the results list
    find_content(nested_json, results)


    # Print the values of "ct_content" keys
    for idx, value in enumerate(results, start=1):
        
        if len(sys.argv) > 3:
            csvwriter.writerow( [idx, value] )
        else:
            print(f"Value {idx}: {value}")
            
    if len(sys.argv) > 3:
        csv_file.close()

if(mode == MODE_OUTPUT_POT):
    
    # Initialize an empty list to store the results
    results = []

    # Call the function to find and store "ct_content" values in the results list
    find_content(nested_json, results)


    # Print the values of "ct_content" keys
    for idx, value in enumerate(results, start=1):
        
        if len(sys.argv) > 3:
            csv_file.write( '#: {0}:{1} \n'.format( os.path.basename(json_filename) ,idx) )
            csv_file.write('msgid "{0}"     \n'.format( value.replace( '"','\"' ) ) )
            csv_file.write('msgstr ""     \n\n')

        else:
            print(f"Value {idx}: {value}")
            
    if len(sys.argv) > 3:
        csv_file.close()

elif(mode == MODE_INPUT):
    
    # making data frame from csv
    data = pd.read_csv( csv_file )
    data.fillna(value='', inplace=True)
    
    translations = data["translation"].tolist()
    
    # Debug only
    if DEBUG:
        for idx, value in enumerate(translations, start=1):
            print(f"Value {idx}: {value}")    
        
    idx = update_content(nested_json, translations)
    if DEBUG:
        print(f"{idx} occurences updated")
            
    if len(sys.argv) == 5:
        json_out_file.write(json.dumps(nested_json))
        json_out_file.close()
    else:
        print(nested_json)
        
elif(mode == MODE_INPUT_POT):
    
    # Initialize an empty list to store the results
    results = []

    # Call the function to find and store "ct_content" values in the results list
    find_content(nested_json, results)
    
    
    data = polib.pofile( csv_filename )
    
    idx = 0

    for entry in data:
        idx += update_po_content(nested_json, entry.msgid, entry.msgstr)

    print(f"{idx} occurences updated out of {len(results)} found.")
            
    if len(sys.argv) == 5:
        json_out_file.write(json.dumps(nested_json))
        json_out_file.close()
    else:
        print(nested_json)
    
json_file.close()

sys.exit()
    
