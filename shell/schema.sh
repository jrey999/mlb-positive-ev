#!/bin/bash
script_dir="$(cd "$(dirname "$0")" && pwd)"; folder="$script_dir/../data/schema/tables"
tables=($(sqlite3 db.sqlite3 ".table"))
for file in "$folder"/*; do
    table="${file##*/}"; table="${table%.sql}"  # split the file so it has the same name as the table
    # Check if the table exists
    if [[ " ${tables[*]} " == *" $table "* ]]; then
    echo "Table '$table' has already been created"
    else
        sqlite3 db.sqlite3 < $file
        echo "Table '$table' was just created"
    fi
done