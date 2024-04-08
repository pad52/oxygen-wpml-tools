#!/bin/bash

################### VARS

SSH_USER=utente
SSH_HOST=localhost
SSH_PORT=22

SSH="$SSH_USER@$SSH_HOST:$SSH_PORT"
WP_PATH="/home/$USER/www/public_html"


WP_CMD="wp --ssh=$SSH$WP_PATH"

SOURCE_LANG="it"
DEST_LANG="fr"

SOURCE_FOLDER="./jsons/*.json"
PO_FILE="../texts/pots/oxygen-pages_$DEST_LANG.po"

#Global
#regex='([a-z]{2})-(page|ct_template)\.([^\.]+)\.([0-9]+)\.([a-z]{2})?\.([0-9]+)\.json'

#Page only
regex='([a-z]{2})-(page)\.([^\.]+)\.([0-9]+)\.([a-z]{2})?\.([0-9]+)\.json'


################### Script start

unmatched=""

if [ ! -f $PO_FILE ]; then
    echo "File $PO_FILE does not exist."
    exit
fi

for f in $SOURCE_FOLDER; do
    # Example filename
    filename=$(basename -- "$f")

    if [[ $filename =~ $regex ]]; then
        lang="${BASH_REMATCH[1]}"
        type="${BASH_REMATCH[2]}"
        slug="${BASH_REMATCH[3]}"
        id="${BASH_REMATCH[4]}"
        slang="${BASH_REMATCH[5]}"
        trid="${BASH_REMATCH[6]}"
#         echo "filename: $filename"
#         echo "lang: $lang type: $type slug: $slug id: $id slang: $slang trid: $trid"
        
        if [[ $lang == $SOURCE_LANG ]]; then

            for ff in $SOURCE_FOLDER; do
                # Example filename
                ffilename=$(basename -- "$ff")

                if [[ $ffilename =~ $regex ]]; then
                    flang="${BASH_REMATCH[1]}"
                    ftype="${BASH_REMATCH[2]}"
                    fslug="${BASH_REMATCH[3]}"
                    fid="${BASH_REMATCH[4]}"
                    fslang="${BASH_REMATCH[5]}"
                    ftrid="${BASH_REMATCH[6]}"
                                        
                    if [[ $flang == $DEST_LANG && $ftrid == $trid ]]; then
                        echo "Updating $ffilename using original $filename"
#                         echo "going to update $fslug with id $fid with original $slug with id $id"
                        ./oxy_translator.py -j $f $PO_FILE $ff
                        
#                         echo "Now updating $flug with id $fid"
                        eval "cat $ff | $WP_CMD post meta update $fid 'ct_builder_json'"
                        
#                         echo "done $flug Press any key to continue..."
#                         read -s -n 1
                    fi                    
                fi
            done
        fi
    else
        unmatched="$filename, $unmatched"
    fi
done

echo "unmatched filenames: $unmatched"
