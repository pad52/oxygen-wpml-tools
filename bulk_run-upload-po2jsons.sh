#!/bin/bash

################### VARS

#SSH connection configuration
SSH_USER=user
SSH_HOST=localhost
SSH_PORT=22

#WP installation path on the remote server
WP_PATH="/home/$USER/www/public_html"

#WP CLI commands
SSH="$SSH_USER@$SSH_HOST:$SSH_PORT"
WP_CMD="wp --ssh=$SSH$WP_PATH"

#Source translation language
SOURCE_LANG="it"

#Available translations
AVAIL_DEST_LANGS=("en" "es" "fr" "de")

#JSONs source folder
SOURCE_FOLDER="./jsons/*.json"

#Enable for Page and Templates
#regex='([a-z]{2})-(page|ct_template)\.([^\.]+)\.([0-9]+)\.([a-z]{2})?\.([0-9]+)\.json'

#Enable for Page only
regex='([a-z]{2})-(page)\.([^\.]+)\.([0-9]+)\.([a-z]{2})?\.([0-9]+)\.json'


################### START

for dest_lang in ${AVAIL_DEST_LANGS[@]}; do

    po_file="../texts/pots/oxygen-pages_$dest_lang.po"

    if [ ! -f $po_file ]; then
        echo "File $po_file does not exist."
        continue
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

                        if [[ $flang == $dest_lang && $ftrid == $trid ]]; then
                            echo "Updating $ffilename using original $filename"
    #                         echo "going to update $fslug with id $fid with original $slug with id $id"
    #                         echo "Doing ./oxy_translator.py -j $f $po_file $ff"
                            ./oxy_translator.py -j $f $po_file $ff
    #                         echo "Now updating $flug with id $fid"
                            eval "cat $ff | $WP_CMD post meta update $fid 'ct_builder_json'"
    #                         echo "done $flug Press any key to continue..."
    #                         read -s -n 1
                        fi
                    fi
                done
            fi
        else
            echo "unmatched filename: $filename"
        fi
    done
done

