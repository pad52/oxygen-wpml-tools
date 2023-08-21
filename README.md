# oxygen-wpml-tools
Tools for automating translation process between Oxygen builder and WPML

Since I don't want to copy/paste every translated text field from a page to another inside the Oxygen Builder,
I just made a very simple python script to automate at least the translation process.
(you will keep doing copy paste between the JSON of a page to the JSON of the translated page)
Hope it helps someone.

# oxy_translator.py
Script that can import/export contents and links from/to an Oxygen JSON file to/from a CSV file.

Usage is the following:

    Go to the Original, not translated page in the "Edit page" Wordpress backend (!not Edit with Oxygen),
    Copy the JSON tab content (Yes you need to have the page ready, done with oxygen)
    Paste it to file. I am using the Linux command line: "xclip -selection clipboard -o > original.json"
    Run the script: "./oxy_translator.py -o original.json original.csv"
    Edit original.csv filling the "translation" column and save it, for example in translated.csv
    Run the script: "./oxy_translator.py -i original.json translated.csv translated.json
    Copy the content of translated.json to clipboard. Using Linux "cat translated.json | xclip -selection clipboard"
    Go to the Translated page in the "Edit page" Wordpress backend
    Paste your clipboard in the JSON tab content.
    Save!

TODO:

     Export in a single .POT file, import from single .PO file in order to use normal translation softwares.


# oxy_json_exporter.php
Script that dumps from the database every JSON in every language 

Usage is the following:

    Upload the script somewhere in your wp installation
    visit the script address from the browser or from the command line using php interpreter
    donwload the JSONs generated 

TODO:

    BUG fixes!
    transform in a WP plugin
    
