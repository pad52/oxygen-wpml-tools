# oxygen-wpml-tools
Tools for automating translation process between Oxygen builder and WPML

Since I don't want to copy/paste every translated text field from a page to another inside the Oxygen Builder,
I made a very simple python script to automate at the translation process.
~~(you will keep doing copy paste between the JSON of a page to the JSON of the translated page)~~
I just made also a bash script to stop copy pasting and upload everything automatically.

So now the method is the following:
1) Upload _oxy_json_exporter.php_ and execute on your website.
2) Download JSON files.
3) Extract POT file with _oxy_translator.py_
4) Translate with your favorite tool and get .PO files
5) Use _bulk_run-upload-po2jsons.sh_ in order to translate and upload translated text.
6) Enjoy!

Hope it helps someone.

# oxy_json_exporter.php
Script that dumps from the database every JSON in every language 

Usage is the following:

    Upload the script inside your wp installation
    visit the script address from the browser or from the command line using php cli
    download the JSONs generated.

TODO:

    transform in a WP plugin or in something that can be used remotely.

    

# oxy_translator.py
Script that can import/export contents and links from/to an Oxygen JSON file to/from a CSV/POT/PO file.

Usage is the following:

Method 1) extract a POT file out from a JSON file
./oxy_translator.py -p $SOURCE.json $DEST.pot

Method 2) translate a SOURCE_JSON file using a .PO file into a new DEST_JSON file
./oxy_translator.py -j $SOURCE_JSON $PO_FILE $DEST_JSON

CSV Methods are deprecated and should not be used anymore.


# bulk_run-jsons2pot.sh
Extracts a single POT file out from many JSON files.


# bulk_run-po2jsons.sh
Bulk translate of many JSON files using a single PO file.


# bulk_run-upload-po2jsons.sh
Scripts that automatically translates multiple JSON files (exported with _oxy_json_exporter.php_), 
translates them with a PO file and **UPLOAD** automatically in Wordpress!
