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

import sys, json,csv
import pandas as pd

debug = 0

MODE_OUTPUT = 0
MODE_INPUT = 1

search_keys = ["ct_content", "url", "icon_box_heading", "icon_box_text"]


def find_content(json_obj, results_list):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key in search_keys:
                results_list.append(value)
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


if len(sys.argv) < 2:
    print("Usage\n \
        From JSON to CSV: oxy_translator.py -o [JSON INPUT FILE] (optional)[CSV OUTPUT FILE] or\n \
        From CSV to JSON: oxy_translator.py -i [JSON INPUT FILE] [CSV INPUT FILE] (optional)[JSON OUTPUT FILE]\n \
        If the optional [OUTPUT FILE] it is not specified the output will be stdout.")
    sys.exit()
elif len(sys.argv) < 3:
    print("ERROR: Give me a json file at least!")
    sys.exit()
elif len(sys.argv) >= 3:
    if(str(sys.argv[1]) == "-o"):
        mode = MODE_OUTPUT
    
        if len(sys.argv) == 4:
            csv_file = open(str(sys.argv[3]),'w');
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow( ['index','original_language','translation'] )
        elif len(sys.argv) > 4:
            print("ERROR: Too many arguments!")
            sys.exit()
    
    elif(str(sys.argv[1]) == "-i"):
        mode = MODE_INPUT
        
        if( len(sys.argv) == 4 or len(sys.argv) == 5):
            csv_file = open(str(sys.argv[3]),'r');
            if len(sys.argv) == 5:
                json_out_file = open(str(sys.argv[4]),'w');
        elif len(sys.argv) > 5:
            print("ERROR: Too many arguments!")
            sys.exit()
        
    else:
        print("ERROR: Arguments -i or -o accepted only.")
        sys.exit()
        
else:
    print("ERROR: Too many arguments!")
    sys.exit()

 
# Opening JSON file
json_file = open(str(sys.argv[2]))

 
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

elif(mode == MODE_INPUT):
    
    # making data frame from csv
    data = pd.read_csv( csv_file )
    data.fillna(value='', inplace=True)
    
    translations = data["translation"].tolist()
    
    # Debug only
    if debug:
        for idx, value in enumerate(translations, start=1):
            print(f"Value {idx}: {value}")    
        
    idx = update_content(nested_json, translations)
    if debug:
        print(f"{idx} occurences updated")
            
    if len(sys.argv) == 5:
        json_out_file.write(json.dumps(nested_json))
        json_out_file.close()
    else:
        print(nested_json)
    
json_file.close()

sys.exit()
    
